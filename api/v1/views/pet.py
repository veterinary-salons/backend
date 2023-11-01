from icecream import ic
from psycopg2 import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers.pets import PetSerializer
from core.utils import get_customer
from pets.models import Pet
from users.models import CustomerProfile

class PetViewSet(ModelViewSet):
    """Представление питомца."""

    queryset = Pet.objects.select_related("owner")
    serializer_class = PetSerializer

    def list(self, request, *args, **kwargs):
        """Вывод списка всех питомцев владельца по параметру из URL.

        Args:
            request: Объект запроса.
            args: Позиционные аргументы.
            kwargs: Именованные аргументы.

        Returns:
            Response: Список всех питомцев владельца.
        """

        owner_pets = self.queryset.filter(owner__id=kwargs["customer_id"])
        serializer = PetSerializer(owner_pets, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Создание питомца.

        Args:
            request: Объект запроса.
            args: Позиционные аргументы.
            kwargs: Именованные аргументы.

        Returns:
            Response: Созданный питомец.

        Raises:
            Response(status=status.HTTP_403_FORBIDDEN): Если питомец создается
            у другого пользователя.
        """
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
        customer_profile = get_customer(self.request)
        try:
            serializer.save(owner=customer_profile)
        except IntegrityError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": "У вас уже есть такой питомце!"
                },
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
