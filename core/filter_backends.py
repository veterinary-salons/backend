from typing import Any

from django.db.models import Q
from rest_framework import filters

from api.v1.serializers import FilterServicesSerializer


class ServiceFilterBackend(filters.BaseFilterBackend):

    def get_filtering(self, fields: dict[str, Any]):
        filtering = Q()

        price = fields.get("price")
        pet_type_list = fields.get("pet_type")
        service_type_list = fields.get("service_type")
        serve_at_supplier = fields.get("serve_at_supplier")
        serve_at_customer = fields.get("serve_at_customer")
        date = fields.get("date")

        if price is not None:
            filtering = Q(price__range=(price[0], price[1]))

        if pet_type_list is not None:
            filtering = filtering & Q(pet_type__in=pet_type_list)

        if service_type_list is not None:
            filtering = filtering & Q(service_type__in=service_type_list)

        if serve_at_customer is not None and serve_at_supplier is not None:
            pass
        elif serve_at_supplier is not None:
            filtering = filtering & Q(serve_at_supplier=True)
        elif serve_at_customer is not None:
            filtering = filtering & Q(serve_at_customer=True)

        if date is not None:
            weekday = date.weekday()
            filtering = filtering & Q(working_days__contains=weekday)

        return filtering

    def filter_queryset(self, request, queryset, view):
        serializer = FilterServicesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filtering = self.get_filtering(serializer.validated_data)
        if filtering is None:
            return queryset
        return queryset.filter(filtering)