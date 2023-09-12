from api.v1.views import GroomerViewSet, PetViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()

router.register("pets", PetViewSet, "pets")
router.register("groomer", GroomerViewSet, "groomers")
urlpatterns = (
    path("", include(router.urls)),
    path("profiles/", include("users.urls")),
    path("auth/", include("authentication.urls")),
)
