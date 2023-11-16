from icecream import ic
from rest_framework import viewsets, generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers.users import (
    CustomerSerializer,
    CustomerPatchSerializer,
    SupplierProfileSerializer,
    BookingListSerializer,
    CustomerProfileSerializer,
)
from core.permissions import IsCustomer, IsAuthor
from core.utils import get_customer
from services.models import Booking
from users.models import CustomerProfile, SupplierProfile


class CustomerProfileView(
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
):
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.prefetch_related("related_user")
    permission_classes = [
        IsAuthenticated,
        IsCustomer,
        IsAuthor,
    ]
    lookup_field = "customer_id"

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs["customer_id"]
        try:
            customer = self.get_queryset().get(id=customer_id)
            customer.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data={"message": f"Пользователь {customer} удален"},
            )
        except CustomerProfile.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Пользователь не найден"},
            )

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get("customer_id")
        customer = self.get_queryset().get(id=customer_id)
        serializer = CustomerSerializer(customer, context={"request": request})
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        customer_id = kwargs.get("customer_id")
        customer = self.get_queryset().get(id=customer_id)
        serializer = CustomerPatchSerializer(customer, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SupplierProfileViewSet(viewsets.ModelViewSet):
    """Отображение данных специалиста."""

    queryset = SupplierProfile.objects.prefetch_related("related_user")
    serializer_class = SupplierProfileSerializer

    def list(self, request, *args, **kwargs):
        return Response({"message": "действие запрещено"})


class BaseCustomerBookingListView(generics.ListAPIView):
    queryset = Booking.objects.prefetch_related("customer")
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if get_customer(self.request, CustomerProfile).id == int(
            self.kwargs.get("customer_id")
        ):
            return self.get_bookings()
        else:
            raise serializers.ValidationError(
                "Нельзя посмотреть чужие бронирования!"
            )

    def get_bookings(self):
        pass  # будет переопределено в дочерних классах


class CustomerBookingList(BaseCustomerBookingListView):
    def get_bookings(self):
        return Booking.objects.filter(
            customer=get_customer(self.request, CustomerProfile).id, is_active=True
        )


class CustomerBookingHistoryList(BaseCustomerBookingListView):
    def get_bookings(self):
        return Booking.objects.filter(
            customer=get_customer(self.request, CustomerProfile).id,
            is_done=True,
            is_active=False,
        )
