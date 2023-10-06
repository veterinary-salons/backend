from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView

from api.v1.serializers import (
    PetSerializer,
    BookingServiceSerializer,
    ServiceSerializer,
)
from core.filter_backends import ServiceFilterBackend
from django.contrib.auth import get_user_model


from pets.models import Pet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from services.models import BookingService, Service
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()


class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = Pet.objects.all()
        serializer = PetSerializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        pet = get_object_or_404(self.queryset, owner_id=kwargs["customer_id"])
        serializer = PetSerializer(pet)
        return Response(serializer.data)

class BaseServiceViewSet(ModelViewSet):
    queryset = Service.objects.select_related("supplier")
    permission_classes = [IsAuthenticated,]

    @action(
        methods=["POST"],
        detail=False,
        filter_backends=(ServiceFilterBackend,),
    )
    def filter(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)


class ServiceViewSet(BaseServiceViewSet):
    queryset = Service.objects.select_related("supplier")
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        supplier_profile = SupplierProfile.objects.get(
            related_user=self.request.user
        )
        serializer.save(supplier=supplier_profile)


class BookingServiceViewSet(ModelViewSet):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        customer_profile = CustomerProfile.objects.get(
            related_user=self.request.user
        )
        serializer.save(customer=customer_profile)

class BookingServiceAPIView(generics.CreateAPIView):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer
    permission_classes = [IsAuthenticated,]
    def perform_create(self, serializer):
        customer_profile = CustomerProfile.objects.get(related_user=self.request.user)
        serializer.save(customer=customer_profile)
