from rest_framework import serializers

from pets.models import Pet
from services.models import Groomer


class PetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet
        fields = '__all__'


class GroomerSerializer(serializers.ModelSerializer):

    # def create(self, validated_data):
    #     user = validated_data.pop('user')
    #     price
    #     work_time_from
    #     work_time_to
    #     about
    #     pet_type
    #     grooming_type
    #     duration
    #

    class Meta:
        model = Groomer
        fields = '__all__'

