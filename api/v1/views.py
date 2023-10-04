from django.db.models import QuerySet

from api.v1.serializers import (
    PetSerializer,
    BookingServiceSerializer,
    ServiceSerializer,
)
from core.filter_backends import ServiceFilterBackend
from django.contrib.auth import get_user_model
from django.http import HttpRequest


from pets.models import Pet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from services.models import BookingService, Service
from users.models import SupplierProfile
from django.db.models import QuerySet
User = get_user_model()


class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    @action(
        methods=["GET"], 
        detail=False, 
        permission_classes=[IsAuthenticated],
    )
    def me(self, request: HttpRequest) -> Response:
        """Показываем питомцев пользователя, который авторизован.

        Args:
            request: Объект HTTPRequest.

        Returns:
            Объект HTTPResponse.

        """
        # надо бы реализовать удаление питомца
        serializer = self.get_serializer(request.user.pets.all(), many=True)
        return Response(serializer.data)


class BaseServiceViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    @action(
        methods=["GET",],
        detail=False, 
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(
            self.queryset.filter(user=request.user), many=True
        )

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


class BookingServiceViewSet(BaseServiceViewSet):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer

