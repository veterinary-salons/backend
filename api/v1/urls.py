from api.v1.views import (
    PetViewSet,
    BaseServiceViewSet,
    BookingServiceAPIView,
    ServiceAPIView,
)
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
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

# router.register(
#     "suppliers",
#     ServiceAPIView.as_view(),
# )

router.register(
    "services",
    ServiceViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
    path("auth/", include("authentication.v1.urls")),
    re_path(
        "customers/(?P<customer_id>\d+)/booking/(?P<supplier_id>\d+)",
        BookingServiceAPIView.as_view(),
        name="booking",
    ),
    re_path(
        "suppliers/(?P<supplier_id>\d+)",
        ServiceAPIView.as_view(),
        name="service",
    ),
    path("profiles/", include("users.v1.urls")),
    path("", include(router.urls)),
]
