from icecream import ic
from rest_framework.permissions import BasePermission

from core.utils import get_customer, get_supplier
from services.models import Price, Booking
from users.models import CustomerProfile, SupplierProfile


class IsAuthor(BasePermission):
    def has_permission(
        self,
        request,
        view,
    ):
        return (
            int(request.resolver_match.kwargs.get("customer_id"))
            == get_customer(request, CustomerProfile).id
        )


class IsCustomer(BasePermission):
    message = "Только для покупателей!"
    def has_permission(
        self,
        request,
        view,
    ):
        return bool(get_customer(request, CustomerProfile))


class IsMyService(BasePermission):
    message = "Нельзя делать отзывы на услуги, которыми вы не пользовались!"

    def has_permission(
        self,
        request,
        view,
    ):
        price_id = int(request.resolver_match.kwargs.get("price_id"))
        customer = (
            CustomerProfile.objects.prefetch_related("bookings__price")
            .filter(bookings__price__id=price_id)
            .first()
        )
        return get_customer(request, CustomerProfile) == customer

class IsSupplier(BasePermission):
    def has_permission(
        self,
        request,
        view,
    ):
        return bool(get_supplier(request, SupplierProfile))
