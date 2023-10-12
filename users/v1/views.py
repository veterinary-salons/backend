from icecream import ic
from rest_framework import viewsets
from rest_framework.response import Response

from users.models import CustomerProfile, SupplierProfile
from users.v1.serializers import (
    CustomerProfileSerializer,
    SupplierProfileSerializer,
    CustomerSerializer,
)

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.select_related("related_user")
    serializer_class = CustomerProfileSerializer

    def list(self, request, *args, **kwargs):
        return Response({"message": "действие запрещено"})


class SupplierProfileViewSet(viewsets.ModelViewSet):
    """Отображение данных специалиста."""
    queryset = SupplierProfile.objects.select_related("related_user")
    serializer_class = SupplierProfileSerializer

    def list(self, request, *args, **kwargs):
        return Response({"message": "действие запрещено"})
