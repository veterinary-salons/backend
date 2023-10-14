from rest_framework import viewsets
from rest_framework.response import Response

from api.v1.serializers.users import (
    CustomerSerializer,
    CustomerPatchSerializer,
    SupplierProfileSerializer,
)
from users.models import CustomerProfile, SupplierProfile

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
