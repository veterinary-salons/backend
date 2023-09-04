from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import PetSerializer, GroomerSerializer
from pets.models import Pet
from services.models import Groomer


class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


class GroomerViewSet(ModelViewSet):
    queryset = Groomer.objects.all()
    serializer_class = GroomerSerializer
