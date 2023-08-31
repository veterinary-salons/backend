from rest_framework import viewsets

from users.models import User, CustomerProfile, SupplierProfile
from users.serializers import (
    CustomerProfileSerializer, SupplierProfileSerializer
)


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.prefetch_related("related_user")
    serializer_class = CustomerProfileSerializer


class SupplierProfileViewSet(viewsets.ModelViewSet):
    queryset = SupplierProfile.objects.prefetch_related("related_user")
    serializer_class = SupplierProfileSerializer