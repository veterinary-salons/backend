from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import ObtainAuthToken

from .views import CustomerProfileViewSet, SupplierProfileViewSet


router = SimpleRouter()
router.register("customers", CustomerProfileViewSet)
router.register("suppliers", SupplierProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token", ObtainAuthToken.as_view()),
]
