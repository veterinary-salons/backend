from copy import deepcopy

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views import View
from icecream import ic
from rest_framework import generics, status, serializers
from rest_framework.mixins import DestroyModelMixin

from api.v1.serializers.core import PriceSerializer
from api.v1.serializers.pets import PetSerializer
from api.v1.serializers.service import (
    BookingSerializer,
    ServiceCreateSerializer,
    ServiceUpdateSerializer,
    BaseServiceSerializer,
    ReviewSerializer,
    FavoriteSerializer,
    SmallServiceSerializer,
    FavoriteArticlesSerializer,
)
from api.v1.serializers.users import (
    CustomerProfileSerializer,
    SupplierProfileSerializer,
)
from core.filter_backends import ServiceFilterBackend
from django.contrib.auth import get_user_model

from core.permissions import IsCustomer, IsAuthor, IsMyService
from core.utils import get_customer
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pets.models import Pet
from services.models import (
    Booking,
    Service,
    Price,
    Favorite,
    Review,
    FavoriteArticles,
)
from users.models import SupplierProfile, CustomerProfile


User = get_user_model()


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


class SupplierServiceProfileView(
    generics.ListCreateAPIView,
    DestroyModelMixin,
):
    """Представление для услуг."""

    queryset = Service.objects.prefetch_related("supplier")
    serializer_class = BaseServiceSerializer

    # def perform_create(self, serializer):
    #     """Добавляем пользователя в вывод сериализатора."""
    #     ic(self.kwargs)
    #     serializer.is_valid(raise_exception=True)
    #     supplier_profile = SupplierProfile.objects.get(
    #         related_user=User.objects.get(id=self.kwargs.get("pk"))
    #     )
    #     serializer.save(supplier=supplier_profile)

    def get(self, request, *args, **kwargs):
        """Выводим услуги конкретного специалиста."""
        supplier_id = int(self.kwargs.get("supplier_id"))
        serializer = self.get_serializer(
            self.queryset.filter(supplier=supplier_id), many=True
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


class BookingServiceAPIView(generics.CreateAPIView):
    """Представление для бронирования."""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        prices = request.data.pop("price", [])
        pet_data = request.data.pop("pet", None)
        _pet_data = deepcopy(pet_data)
        _pet_data.pop("age", None)
        customer_profile = get_customer(self.request)
        try:
            pet = Pet.objects.get(**_pet_data, owner=get_customer(self.request))
            pet_serializer = PetSerializer(pet)
            # создаем питомца, но если уже есть питомцы, то фигня какая то, подумать и поправить.
        except Pet.DoesNotExist:
            pet_serializer = PetSerializer(data=pet_data)
            pet_serializer.is_valid(raise_exception=True)
            pet_serializer.save(owner=customer_profile,)
        bookings = []
        for price in prices:
            booking = Booking.objects.create(
                price_id=price,
                is_active=True,
                customer=customer_profile,
                **request.data,
            )
            bookings.append(booking)
        serialized_data = []
        for booking in bookings:
            serializer = BookingSerializer(booking)
            booking_data = serializer.data
            booking_data["customer"] = CustomerProfileSerializer(
                booking.customer
            ).data
            booking_data["price"] = PriceSerializer(booking.price).data
            serialized_data.append(booking_data)
        serialized_data.append({"pet": pet_serializer.data})
        return Response(serialized_data)


class SupplierCreateAdvertisement(
    generics.DestroyAPIView, generics.CreateAPIView, generics.UpdateAPIView
):
    """Представление для создания объявления."""

    queryset = Service.objects.prefetch_related("supplier")
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(
        self, serializer: ServiceCreateSerializer | ServiceUpdateSerializer
    ):
        """Сохраняем расписание."""
        supplier_profile = SupplierProfile.objects.get(
            related_user=self.request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(supplier=supplier_profile)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ServiceCreateSerializer
        elif self.request.method == "PATCH":
            return ServiceUpdateSerializer


class BookingReviewCreateOrDelete(View):
    def get(self, request, *args, **kwargs):
        view = ReviewCreateView.as_view()
        return view(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        view = BookingCancelView.as_view()
        return view(request, *args, **kwargs)


class ReviewCreateView(generics.CreateAPIView):
    """Представление для создания отзыва."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomer, IsAuthor, IsMyService]

    def create(self, request, *args, **kwargs):
        price_id = int(kwargs.get("price_id"))
        request.data["price_id"] = price_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        price = Price.objects.get(id=price_id)
        price_serializer = PriceSerializer(price)
        data = serializer.data
        data["price"] = price_serializer.data

        customer = CustomerProfile.objects.get(
            id=int(kwargs.get("customer_id"))
        )
        data["customer"] = CustomerProfileSerializer(customer).data
        data["service_date"] = (
            Booking.objects.filter(
                customer=customer,
                price=price,
                is_active=False,
            )
            .first()
            .to_date
        )
        return Response(data)


class BookingCancelView(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomer, IsAuthor, IsMyService]

    def delete(self, request, *args, **kwargs):
        price_id = int(kwargs.get("price_id"))
        booking = Booking.objects.filter(
            price_id=price_id,
            is_active=True,
            customer=get_customer(request),
        )
        if not booking.exists():
            raise serializers.ValidationError(
                "Бронирование уже было отменено или его и не было."
            )
        booking.update(
            is_cancelled=True,
            is_active=False,
            is_done=False,
        )
        booking = Booking.objects.filter(
            price_id=price_id,
            is_active=False,
            customer=get_customer(request),
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"message": f"Бронирование {booking.first()} отменено"},
        )


class FavoriteServiceView(
    generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView
):
    """Представление для добавления в избранное."""

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    lookup_field = "customer_id"

    def get_queryset(self):
        return Favorite.objects.filter(customer=get_customer(self.request))

    def perform_create(self, serializer):
        customer = get_customer(self.request)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer)
        return serializer

    def get(self, request, *args, **kwargs):
        customer = get_customer(self.request)
        services = Service.objects.filter(
            in_favorites__customer=customer,
        )
        serialized_data = []
        for service in services:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            data = serializer
            supplier = SupplierProfile.objects.get(
                id=service.supplier.id,
            )
            review = Review.objects.filter(service=service)
            price = Price.objects.filter(
                service=service,
            )
            data["service"] = SmallServiceSerializer(service).data
            data["price"] = PriceSerializer(price, many=True).data
            data["supplier"] = SupplierProfileSerializer(supplier).data

            if review.exists():
                data["review"] = ReviewSerializer(
                    review.data,
                    many=True,
                )
            else:
                data["review"] = "Отзывов пока нет."
            serialized_data.append(data)

        return Response(serialized_data)


class FavoriteArticlesView(
    generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView
):
    """Представление для добавления статей в избранное."""

    serializer_class = FavoriteArticlesSerializer
    permission_classes = [
        IsAuthenticated,
        IsCustomer,
        IsAuthor,
    ]
    lookup_field = "customer_id"

    def get_queryset(self):
        return FavoriteArticles.objects.filter(
            customer=get_customer(self.request)
        )

    def perform_create(self, serializer):
        customer = get_customer(self.request)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer)
        return serializer

    def delete(self, request, *args, **kwargs):
        customer = get_customer(self.request)
        article_id = int(request.data.get("article_id"))
        articles = FavoriteArticles.objects.filter(
            customer=customer,
            article_id=article_id,
        )
        if articles.exists():
            articles.delete()
        else:
            raise serializers.ValidationError(
                f"Статья {article_id} уже была удалена из избранного или ее там и не было."
            )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"message": f"Статья {article_id} удалена"},
        )
