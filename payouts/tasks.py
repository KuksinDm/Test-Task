import logging
import time

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Payout

logger = logging.getLogger("celery")


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_payout_task(self, payout_id: int) -> None:
    try:
        with transaction.atomic():
            payout = (
                Payout.objects.select_for_update()
                .only("id", "status")
                .get(id=payout_id)
            )
            if payout.status != Payout.Status.NEW:
                return
            payout.status = Payout.Status.PROCESSING
            payout.save(update_fields=["status", "updated_at"])
    except Payout.DoesNotExist:
        logger.warning("Payout not found", extra={"payout_id": payout_id})
        return

    # Имитация обработки
    time.sleep(1)

    with transaction.atomic():
        payout = (
            Payout.objects.select_for_update().only("id", "status").get(id=payout_id)
        )
        if payout.status != Payout.Status.PROCESSING:
            return
        payout.status = Payout.Status.APPROVED
        payout.processed_at = timezone.now()
        payout.error_message = None
        payout.save(
            update_fields=["status", "processed_at", "error_message", "updated_at"]
        )
    logger.info("Payout processed", extra={"payout_id": payout_id})
