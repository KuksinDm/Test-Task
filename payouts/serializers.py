from decimal import Decimal

from rest_framework import serializers

from .models import Payout
from .validators import (
    validate_amount,
    validate_recipient_details,
    validate_status_transition,
)


class PayoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = (
            "external_id",
            "amount",
            "currency",
            "recipient_details",
            "description",
        )
        extra_kwargs = {
            "external_id": {"required": False},
            "description": {"required": False, "allow_blank": True},
        }

    def validate_amount(self, value: Decimal) -> Decimal:
        return validate_amount(value)

    def validate_recipient_details(self, value: str) -> str:
        return validate_recipient_details(value)


class PayoutUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ("status", "description", "recipient_details")
        extra_kwargs = {
            "description": {"required": False, "allow_blank": True},
            "recipient_details": {"required": False},
            "status": {"required": False},
        }

    def validate_status(self, value: str) -> str:
        instance = self.instance
        if instance:
            validate_status_transition(instance.status, value)
        return value

    def validate_recipient_details(self, value: str) -> str:
        return validate_recipient_details(value)


class PayoutReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = "__all__"
        read_only_fields = (
            "id",
            "external_id",
            "status",
            "processed_at",
            "error_message",
            "created_at",
            "updated_at",
        )
