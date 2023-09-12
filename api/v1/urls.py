from api.v1.views import GroomerViewSet, PetViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register("pets", PetViewSet)

urlpatterns = [
    path("auth/", include("authentication.v1.urls")),
    path("profiles/", include("users.v1.urls")),
    path("services/", include("services.v1.urls")),
    path("", include(router.urls)),
]
