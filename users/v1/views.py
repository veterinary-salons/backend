from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.models import CustomerProfile, SupplierProfile
from users.v1.serializers import (CustomerProfileSerializer,
                               SupplierProfileSerializer)
from api.v1.serializers import PetSerializer
from pets.models import Pet


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.prefetch_related("related_user")
    serializer_class = CustomerProfileSerializer


class SupplierProfileViewSet(viewsets.ModelViewSet):
    queryset = SupplierProfile.objects.prefetch_related("related_user")
    serializer_class = SupplierProfileSerializer

    @action(methods=["GET"], detail=True, permission_classes=[IsAuthenticated])
    def grooming(self, request):
        pass
