import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Payout(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        PROCESSING = "processing", "Processing"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        FAILED = "failed", "Failed"

    class Currency(models.TextChoices):
        RUB = "RUB", "Ruble"
        USD = "USD", "US Dollar"
        EUR = "EUR", "Euro"

    external_id = models.UUIDField(unique=True, default=uuid.uuid4, db_index=True)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    currency = models.CharField(max_length=3, choices=Currency.choices)
    recipient_details = models.TextField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    description = models.TextField(blank=True)
    error_message = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payout"
        verbose_name_plural = "Payouts"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="payout_amount_gt_zero",
            ),
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["-created_at"]),
        ]
