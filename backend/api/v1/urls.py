from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import PetViewSet

router = DefaultRouter()

router.register('pets', PetViewSet, 'pets')

urlpatterns = (
    path('', include(router.urls)),
)
