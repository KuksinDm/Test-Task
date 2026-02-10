from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from .serializers import (
    PayoutCreateSerializer,
    PayoutReadSerializer,
    PayoutUpdateSerializer,
)

PAYOUTS_SCHEMA = extend_schema_view(
    list=extend_schema(
        tags=["Payouts"],
        summary="Список заявок",
        responses={200: PayoutReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["Payouts"],
        summary="Детали заявки",
        responses={200: PayoutReadSerializer},
    ),
    create=extend_schema(
        tags=["Payouts"],
        summary="Создать заявку",
        request=PayoutCreateSerializer,
        responses={201: PayoutReadSerializer},
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        tags=["Payouts"],
        summary="Обновить статус заявки",
        request=PayoutUpdateSerializer,
        responses={200: PayoutReadSerializer},
    ),
    destroy=extend_schema(
        tags=["Payouts"],
        summary="Удалить заявку",
        responses={204: None},
    ),
)
