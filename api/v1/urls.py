from api.v1.views import (
    PetViewSet,
    ServiceViewSet,
    BaseServiceViewSet,
    BookingServiceAPIView,
    # BookingServiceAPIView,
)  # BookingServiceViewSet, ServiceViewSet
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register(
    "profiles/customers/(?P<customer_id>\d+)/pet",
    PetViewSet,
    basename="petviewset",
)
router.register(
    "services/${serviceType}",
    BaseServiceViewSet,
)

# router.register(
#     "profiles/customers/(?P<customer_id>\d+)/booking/(?P<supplier_id>\d+)",
#     BookingServiceAPIView.as_view(),
#     name = "bookingview"
# )
router.register(
    "services",
    ServiceViewSet,
)

urlpatterns = [
    path("auth/", include("authentication.v1.urls")),
    re_path(
        "customers/(?P<customer_id>\d+)/booking/(?P<supplier_id>\d+)",
        BookingServiceAPIView.as_view(),
        name="booking",
    ),
    path("profiles/", include("users.v1.urls")),
    path("", include(router.urls)),
]
