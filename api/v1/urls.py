from api.v1.views import PetViewSet, BookingServiceViewSet, ServiceViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register("pets", PetViewSet)
router.register("booking", BookingServiceViewSet)
router.register("services", ServiceViewSet)

urlpatterns = [
    path("auth/", include("authentication.v1.urls")),
    path("profiles/", include("users.v1.urls")),
    path("", include(router.urls)),
]
