from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import PetViewSet, GroomerViewSet

app_name = 'api'

router = DefaultRouter()

router.register('pets', PetViewSet, 'pets')
router.register("groomer", GroomerViewSet, "groomers")
urlpatterns = (
    path('', include(router.urls)),
)
