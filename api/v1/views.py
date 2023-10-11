from django.db import transaction
from django.shortcuts import get_object_or_404
from icecream import ic
from rest_framework import generics, status
from rest_framework.views import APIView

from api.v1.serializers import (
    PetSerializer,
    BookingSerializer,
    ServiceSerializer,
    BookingServiceRetrieveSerializer,
    AgeSerializer,
)
from core.filter_backends import ServiceFilterBackend
from django.contrib.auth import get_user_model


from pets.models import Pet, Age
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from services.models import Booking, Service
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()


class PetViewSet(ModelViewSet):
    queryset = Pet.objects.select_related("owner")
    serializer_class = PetSerializer

    def list(self, request, *args, **kwargs):
        owner_pets = self.queryset.filter(owner__id=kwargs["customer_id"])
        serializer = PetSerializer(owner_pets, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if CustomerProfile.objects.get(
            related_user=self.request.user
        ).id != int(kwargs["customer_id"]):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_profile = CustomerProfile.objects.get(
            related_user=self.request.user
        )
        serializer.save(owner=customer_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BaseServiceViewSet(ModelViewSet):
    queryset = Service.objects.select_related("supplier")
    permission_classes = [
        # IsAuthenticated,
    ]

    @action(
        methods=["POST"],
        detail=False,
        filter_backends=(ServiceFilterBackend,),
    )
    def filter(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)


class ServiceAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.select_related("supplier")
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        supplier_profile = SupplierProfile.objects.get(
            related_user=self.request.user
        )
        serializer.save(supplier=supplier_profile)

    def get(self, request, *args, **kwargs):
        ic(self.queryset)
        supplier_id = int(self.kwargs.get("supplier_id"))
        services = self.queryset.filter(supplier=supplier_id)
        ic(services)
        ic(ServiceSerializer(services, many=True))
        serializer = ServiceSerializer(services, many=True)
        return Response(data=serializer.data)
        # return Response(data=serializers_data)


class BookingServiceAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        customer_profile = CustomerProfile.objects.get(
            related_user=self.request.user,
        )
        supplier_id = self.kwargs.get("supplier_id")
        supplier_profile = SupplierProfile.objects.get(id=supplier_id)
        serializer.save(
            customer=customer_profile,
            supplier=supplier_profile,
        )
