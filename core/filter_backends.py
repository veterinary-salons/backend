from typing import Any

from django.db.models import Q
from icecream import ic
from rest_framework import filters

from api.v1.serializers.service import FilterServicesSerializer
from core.utils import string_to_boolean
from services.models import Service


class ServiceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}

        cost_from = request.query_params.get("cost_from")
        if cost_from:
            filters["prices__cost_from__gte"] = int(cost_from)

        cost_to = request.query_params.get("cost_to")
        if cost_to:
            filters["prices__cost_from__lte"] = int(cost_to)

        category = request.query_params.get("category")
        if category:
            filters["category"] = category

        supplier_place = string_to_boolean(
            request.query_params.get("supplier_place")
        )
        if supplier_place is not None:
            filters["supplier_place"] = supplier_place

        customer_place = string_to_boolean(
            request.query_params.get("customer_place")
        )
        if customer_place is not None:
            filters["customer_place"] = customer_place

        service_name = request.query_params.get("service_name", None)
        if service_name is not None:
            filters["extra_fields__service_name__contains"] = [service_name]
        return queryset.filter(**filters)
