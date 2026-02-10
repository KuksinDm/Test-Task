from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from django.db import transaction
from django.utils import timezone

from .models import Payout
from .validators import validate_status_transition


@dataclass(frozen=True)
class PayoutProcessResult:
    status: str
    error_message: Optional[str] = None


class PayoutService:
    @staticmethod
    @transaction.atomic
    def create_payout(**data) -> Payout:
        payout = Payout.objects.create(**data)
        # Запуск фоновой задачи после создания
        from .tasks import process_payout_task

        process_payout_task.delay(payout.id)
        return payout

    @staticmethod
    @transaction.atomic
    def update_status(
        payout: Payout, new_status: str, error_message: str | None = None
    ) -> Payout:
        validate_status_transition(payout.status, new_status)

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
        return payout
