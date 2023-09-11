from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.v1.views import CustomerProfileViewSet, SupplierProfileViewSet

router = SimpleRouter()
router.register("customers", CustomerProfileViewSet)
router.register("suppliers", SupplierProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
