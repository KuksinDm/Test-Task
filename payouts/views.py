from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Payout
from .schemas import PAYOUTS_SCHEMA
from .serializers import (
    PayoutCreateSerializer,
    PayoutReadSerializer,
    PayoutUpdateSerializer,
)
from .services import PayoutService


@PAYOUTS_SCHEMA
class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutReadSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PayoutCreateSerializer
        if self.action in {"update", "partial_update"}:
            return PayoutUpdateSerializer
        return PayoutReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payout = PayoutService.create_payout(**serializer.validated_data)
        read_serializer = PayoutReadSerializer(
            payout, context=self.get_serializer_context()
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        payout = PayoutService.update_status(
            instance, serializer.validated_data["status"]
        )
        read_serializer = PayoutReadSerializer(
            payout, context=self.get_serializer_context()
        )
        return Response(read_serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
