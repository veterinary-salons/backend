from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    CustomerProfileViewSet, SupplierProfileViewSet, CustomObtainAuthToken
)


router = SimpleRouter()
router.register("customers", CustomerProfileViewSet)
router.register("suppliers", SupplierProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token", CustomObtainAuthToken.as_view()),
]
