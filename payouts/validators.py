from decimal import Decimal

from rest_framework import serializers

from .models import Payout


def validate_amount(value: Decimal) -> Decimal:
    if value <= 0:
        raise serializers.ValidationError("Сумма должна быть положительной.")
    return value


def validate_recipient_details(value: str) -> str:
    value = value.strip()
    if not value:
        raise serializers.ValidationError("Реквизиты обязательны.")
    if len(value) > 2000:
        raise serializers.ValidationError("Реквизиты слишком длинные.")
    return value


def validate_status_transition(current: str, new: str) -> None:
    allowed = {
        Payout.Status.NEW: {Payout.Status.PROCESSING, Payout.Status.REJECTED},
        Payout.Status.PROCESSING: {Payout.Status.APPROVED, Payout.Status.FAILED},
        Payout.Status.APPROVED: set(),
        Payout.Status.REJECTED: set(),
        Payout.Status.FAILED: set(),
    }
    if new == current:
        return
    if new not in allowed.get(current, set()):
        raise serializers.ValidationError(
            f"Недопустимый переход статуса: {current} → {new}."
        )
