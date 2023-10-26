from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.mixins import DestroyModelMixin

from api.v1.serializers.pets import PetSerializer
from api.v1.serializers.service import (
    BookingSerializer,
    ServiceCreateSerializer,
    ServiceUpdateSerializer,
)
from core.filter_backends import ServiceFilterBackend
from django.contrib.auth import get_user_model

from pets.models import Pet
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
    """Представление питомца."""

    queryset = Pet.objects.select_related("owner")
    serializer_class = PetSerializer

    def list(self, request, *args, **kwargs):
        """Вывод списка всех питомцев владельца по параметру из URL."""

        owner_pets = self.queryset.filter(owner__id=kwargs["customer_id"])
        serializer = PetSerializer(owner_pets, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Создание питомца."""
        if CustomerProfile.objects.get(
            related_user=self.request.user
        ).id != int(kwargs["customer_id"]):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    "error": "Нельзя создать питомца у другого пользователя!"
                },
            )
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_profile = CustomerProfile.objects.get(
            related_user=self.request.user
        )
        serializer.save(owner=customer_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BaseServiceViewSet(ModelViewSet):
    queryset = Service.objects.select_related("supplier")
    serializer_class = ServiceCreateSerializer
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


class SupplierProfileView(
    generics.ListCreateAPIView,
    DestroyModelMixin,
):
    """Представление для услуг."""

    queryset = Service.objects.prefetch_related("supplier")
    serializer_class = ServiceCreateSerializer

    def perform_create(self, serializer):
        """Добавляем пользователя в вывод сериализатора."""

        serializer.is_valid(raise_exception=True)
        supplier_profile = SupplierProfile.objects.get(
            related_user=self.request.user
        )
        serializer.save(supplier=supplier_profile)

    def get(self, request, *args, **kwargs):
        """Выводим услуги конкретного специалиста."""

        supplier_id = int(self.kwargs.get("supplier_id"))
        serializer = ServiceCreateSerializer(
            self.queryset.filter(supplier=supplier_id),
            many=True,
        )
        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        """Удаляем специалиста и, заодно, все услуги."""
        supplier_id = int(self.kwargs.get("supplier_id"))
        supplier = SupplierProfile.objects.filter(id=supplier_id)
        last_name = get_object_or_404(supplier).user.last_name
        first_name = get_object_or_404(supplier).user.first_name
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"message": f"Пользователь {last_name} {first_name} удален"},
        )


class BookingServiceAPIView(generics.CreateAPIView,):
    """Представление для бронирования."""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        """Добавляем в вывод сериалиализатора заказчика и специалиста."""

        customer_profile = CustomerProfile.objects.get(
            related_user=self.request.user,
        )
        supplier_id = self.kwargs.get("supplier_id")
        supplier_profile = SupplierProfile.objects.get(id=supplier_id)
        serializer.save(
            customer=customer_profile,
            supplier=supplier_profile,
        )


class SupplierCreateAdvertisement(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """Представление для создания объявления."""

    queryset = Service.objects.prefetch_related("supplier")
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer: ServiceCreateSerializer | ServiceUpdateSerializer):
        """Сохраняем расписание."""
        supplier_profile = SupplierProfile.objects.get(
            related_user=self.request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(supplier=supplier_profile)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceCreateSerializer
        elif self.request.method == 'PATCH':
            return ServiceUpdateSerializer
