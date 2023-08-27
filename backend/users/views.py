from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken

from .models import User, CustomerProfile, SupplierProfile
from .serializers import (
    CustomerProfileSerializer, SupplierProfileSerializer,
    CustomAuthTokenSerializer,
)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.prefetch_related("related_user")
    serializer_class = CustomerProfileSerializer


class SupplierProfileViewSet(viewsets.ModelViewSet):
    queryset = SupplierProfile.objects.prefetch_related("related_user")
    serializer_class = SupplierProfileSerializer