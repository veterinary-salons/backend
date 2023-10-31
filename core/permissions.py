from rest_framework.permissions import BasePermission

from core.utils import get_customer


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.price.customer == get_customer(request)

class IsCustomer(BasePermission):
    def has_permission(self, request, view,):
        return bool(get_customer(request))
