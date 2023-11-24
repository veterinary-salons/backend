from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.v1.views.authentication import (
    SignUpView,
    SignInViewSet,
    VerifyEmailView,
)

from api.v1.views.pet import PetViewSet
from api.v1.views.service import (
    BookingServiceAPIView,
    SupplierServiceProfileView,
    SupplierCreateAdvertisement,
    BookingReviewCreateOrDelete,
    FavoriteServiceView,
    FavoriteArticlesView,
)
from api.v1.views.users import (
    CustomerProfileView,
    SupplierProfileViewSet,
    CustomerBookingList,
    CustomerBookingHistoryList,
)


app_name = "api"

router = DefaultRouter()
router.register(
    "customers/(?P<customer_id>\d+)/profile/pet",
    PetViewSet,
    basename="petviewset",
)

router.register("suppliers", SupplierProfileViewSet, basename="supplier")
# router.register("auth/signup", SignUpView, basename="signup")
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
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        "auth/signup/$",
        SignUpView.as_view(),
        name="signup",
    ),
    re_path(
        "auth/signup/verify_email/$",
        VerifyEmailView.as_view(),
        name="verify_mail",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/booking/(?P<supplier_id>\d+)/$",
        BookingServiceAPIView.as_view(),
        name="booking",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/profile/$",
        CustomerProfileView.as_view(),
        name="customer_profile",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/profile/services/",
        CustomerBookingList.as_view(),
        name="customer_services",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/profile/services/history/$",
        CustomerBookingHistoryList.as_view(),
        name="customer_history_services",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/profile/services/history/(?P<price_id>\d+)/$",
        BookingReviewCreateOrDelete.as_view(),
        name="service_review",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/favorites/services/$",
        FavoriteServiceView.as_view(),
        name="favorite_services",
    ),
    re_path(
        "customers/(?P<customer_id>\d+)/favorites/articles/$",
        FavoriteArticlesView.as_view(),
        name="favorite_articles",
    ),
    re_path(
        "suppliers/(?P<supplier_id>\d+)/profile/$",
        SupplierServiceProfileView.as_view(),
        name="service_get",
    ),
    re_path(
        "booking/suppliers/(?P<supplier_id>\d+)/(?P<pk>\d+)/$",
        SupplierCreateAdvertisement.as_view(),
        name="service_patch",
    ),
    re_path(
        "booking/suppliers/(?P<supplier_id>\d+)/$",
        SupplierCreateAdvertisement.as_view(),
        name="service_post",
    ),
    # re_path(
    #     "services/$",
    #     ServiceFilterView.as_view(),
    #     name="service_filter",
    # ),
    path("auth/token", TokenObtainPairView.as_view()),
    path("auth/refresh-token", TokenRefreshView.as_view()),
]
