from pets.models import Pet
from rest_framework import serializers
from services.models import Groomer


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'


class GroomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groomer
        fields = (
            "price",
            "work_time_from",
            "work_time_to",
            "about",
            "pet_type",
            "grooming_type",
            "duration",
            "published",
        )
