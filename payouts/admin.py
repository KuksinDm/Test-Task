from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Payout


class PayoutResource(resources.ModelResource):
    class Meta:
        model = Payout
        fields = (
            "id",
            "external_id",
            "amount",
            "currency",
            "recipient_details",
            "status",
            "description",
            "error_message",
            "processed_at",
            "created_at",
            "updated_at",
        )


@admin.register(Payout)
class PayoutAdmin(ImportExportModelAdmin):
    resource_class = PayoutResource
    list_display = (
        "id",
        "external_id",
        "amount",
        "currency",
        "status",
        "created_at",
        "processed_at",
    )
    list_filter = ("status", "currency", "created_at")
    search_fields = ("external_id", "recipient_details")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "processed_at")
