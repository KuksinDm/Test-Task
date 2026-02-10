from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from django.db import transaction
from django.utils import timezone

from .models import Payout
from .tasks import process_payout_task
from .validators import validate_status_transition

logger = logging.getLogger("payouts")


@dataclass(frozen=True)
class PayoutProcessResult:
    status: str
    error_message: Optional[str] = None


class PayoutService:
    @staticmethod
    @transaction.atomic
    def create_payout(**data) -> Payout:
        payout = Payout.objects.create(**data)
        logger.info(
            "Payout created",
            extra={
                "payout_id": payout.id,
                "external_id": str(payout.external_id),
                "amount": str(payout.amount),
                "currency": payout.currency,
            },
        )
        # Запуск фоновой задачи после создания
        process_payout_task.delay(payout.id)
        return payout

    @staticmethod
    @transaction.atomic
    def update_status(
        payout: Payout, new_status: str, error_message: str | None = None
    ) -> Payout:
        validate_status_transition(payout.status, new_status)

        old_status = payout.status
        payout.status = new_status
        if new_status in {
            Payout.Status.APPROVED,
            Payout.Status.REJECTED,
            Payout.Status.FAILED,
        }:
            payout.processed_at = timezone.now()
        else:
            payout.processed_at = None

        if new_status == Payout.Status.FAILED:
            payout.error_message = error_message or "Unknown error"
        else:
            payout.error_message = None

        payout.save(
            update_fields=["status", "processed_at", "error_message", "updated_at"]
        )
        logger.info(
            "Payout status updated",
            extra={
                "payout_id": payout.id,
                "external_id": str(payout.external_id),
                "old_status": old_status,
                "new_status": new_status,
            },
        )
        return payout

    @staticmethod
    @transaction.atomic
    def update_payout(
        payout: Payout,
        *,
        status: str | None = None,
        description: str | None = None,
        recipient_details: str | None = None,
    ) -> Payout:
        if status is not None:
            payout = PayoutService.update_status(payout, status)

        update_fields = []
        if description is not None:
            payout.description = description
            update_fields.append("description")
        if recipient_details is not None:
            payout.recipient_details = recipient_details
            update_fields.append("recipient_details")

        if update_fields:
            update_fields.append("updated_at")
            payout.save(update_fields=update_fields)

        return payout
