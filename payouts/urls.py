from rest_framework.routers import DefaultRouter

from .views import PayoutViewSet

router = DefaultRouter()
router.register(r"payouts", PayoutViewSet, basename="payout")

urlpatterns = router.urls
