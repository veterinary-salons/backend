from icecream import ic
from rest_framework import viewsets, generics, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers.users import (
    CustomerSerializer,
    CustomerPatchSerializer,
    SupplierProfileSerializer,
    BookingListSerializer,
)
from core.utils import get_customer
from services.models import Booking
from users.models import CustomerProfile, SupplierProfile


class CustomerProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = CustomerProfile.objects.prefetch_related("related_user")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CustomerSerializer
        elif self.request.method == "PATCH":
            return CustomerPatchSerializer


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
        if get_customer(self.request).id == int(self.kwargs.get("customer_id")):
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
           customer=get_customer(self.request).id,
           is_active=True
        )


class CustomerBookingHistoryList(BaseCustomerBookingListView):

    def get_bookings(self):
        return Booking.objects.filter(
           customer=get_customer(self.request).id,
           is_done=True,
           is_active=False
        )
