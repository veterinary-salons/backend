from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import PetSerializer, GroomerSerializer
from pets.models import Pet
from services.models import Groomer


User = get_user_model()


class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    @action(
        methods=['GET', ],
        detail=False,
        # permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request: HttpRequest) -> Response:
        """Показываем питомцев пользователя, который авторизован.

        Args:
            request: Объект HTTPRequest.

        Returns:
            Объект HTTPResponse.

        """
        # надо бы реализовать удаление питомца
        serializer = PetSerializer(Pet.objects.filter(owner=1), many=True)  # заглушка, пока нет аутентификации.
        return Response(serializer.data)


class GroomerViewSet(ModelViewSet):
    queryset = Groomer.objects.all()
    serializer_class = GroomerSerializer

    def me(self, request: HttpRequest) -> Response:
        """Показываем питомцев пользователя, который авторизован.

        Args:
            request: Объект HTTPRequest.

        Returns:
            Объект HTTPResponse.

        """
        # надо бы реализовать удаление питомца
        user = User(id=1) # еще одна заглушка
        serializer = GroomerSerializer(user.groomers.all(),)  # заглушка, пока нет аутентификации.
        return Response(serializer.data)
