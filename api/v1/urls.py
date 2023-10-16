from django.template.defaulttags import url
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.v1.views.authentication import SignUpViewSet, SignInViewSet
from api.v1.views.service import (
    PetViewSet,
    BaseServiceViewSet,
    BookingServiceAPIView,
    ServiceAPIView,
)
from api.v1.views.users import CustomerProfileViewSet, SupplierProfileViewSet
from backend import settings

app_name = "api"

router = DefaultRouter()
router.register(
    "customers/(?P<customer_id>\d+)/profile/pet",
    PetViewSet,
    basename="petviewset",
)
router.register(
    "services/${serviceType}",
    BaseServiceViewSet,
)
router.register("customers", CustomerProfileViewSet)
router.register("suppliers", SupplierProfileViewSet)

router.register("auth/signup", SignUpViewSet, basename="signup")
router.register("auth/signin", SignInViewSet, basename="signin")

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/booking/(?P<supplier_id>\d+)$",
        BookingServiceAPIView.as_view(),
        name="booking",
    ),
    re_path(
        "suppliers/(?P<supplier_id>\d+)/profile",
        ServiceAPIView.as_view(),
        name="service",
    ),
    path("auth/token", TokenObtainPairView.as_view()),
    path("auth/refresh-token", TokenRefreshView.as_view()),
]

