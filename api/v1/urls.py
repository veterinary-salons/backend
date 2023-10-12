from api.v1.views import (
    PetViewSet,
    BaseServiceViewSet,
    BookingServiceAPIView,
    ServiceAPIView,
)
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register(
    "customers/(?P<customer_id>\d+)/pet",
    PetViewSet,
    basename="petviewset",
)
router.register(
    "services/${serviceType}",
    BaseServiceViewSet,
)

urlpatterns = [
    path("auth/", include("authentication.v1.urls")),
    re_path(
        "customers/(?P<customer_id>\d+)/booking/(?P<supplier_id>\d+)",
        BookingServiceAPIView.as_view(),
        name="booking",
    ),
    re_path(
        "suppliers/(?P<supplier_id>\d+)/profile",
        ServiceAPIView.as_view(),
        name="service",
    ),
    path("", include("users.v1.urls")),
    path("", include(router.urls)),
]
