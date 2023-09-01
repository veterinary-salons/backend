from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import PetSerializer
from pets.models import Pet


class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
