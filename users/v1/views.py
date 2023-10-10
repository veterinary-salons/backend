from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.v1.serializers import SupplierSerializer
from users.models import CustomerProfile, SupplierProfile
from users.v1.serializers import CustomerProfileSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.prefetch_related("related_user")
    serializer_class = CustomerProfileSerializer


class SupplierProfileViewSet(viewsets.ModelViewSet):
    """Отображение профиля специалиста."""
    queryset = SupplierProfile.objects.prefetch_related("related_user")
    serializer_class = SupplierSerializer
    # permission_classes = [IsAuthenticated,]

