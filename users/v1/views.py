from icecream import ic
from rest_framework import viewsets
from rest_framework.response import Response

from users.models import CustomerProfile, SupplierProfile
from users.v1.serializers import (
    CustomerSerializer,
    SupplierProfileSerializer,
    CustomerPatchSerializer,
)

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.prefetch_related("related_user")

    def get_serializer_class(self):
        if self.request.method in ('GET', "POST"):
            return CustomerSerializer
        elif self.request.method == 'PATCH':
            return CustomerPatchSerializer

    def list(self, request, *args, **kwargs):
        return Response({"message": "действие запрещено"})

class SupplierProfileViewSet(viewsets.ModelViewSet):
    """Отображение данных специалиста."""
    queryset = SupplierProfile.objects.prefetch_related("related_user")
    serializer_class = SupplierProfileSerializer

    def list(self, request, *args, **kwargs):
        return Response({"message": "действие запрещено"})
