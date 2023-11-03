from icecream import ic
from rest_framework import serializers

from core.constants import Limits
from pets.models import Age, Pet


class AgeSerializer(serializers.ModelSerializer):
    """Сериализация возраста."""

    class Meta:
        model = Age
        fields = (
            "year",
            "month",
        )

    @staticmethod
    def validate_year(value):
        if value > Limits.MAX_AGE_PET or value < Limits.MIN_AGE_PET:
            raise serializers.ValidationError(
                "Возраст питомца должен быть от "
                f"{Limits.MIN_AGE_PET} до {Limits.MAX_AGE_PET} лет"
            )
        return value

    @staticmethod
    def validate_month(value):
        if value > Limits.MAX_MONTH_QUANTITY or value < 0:
            raise serializers.ValidationError(
                "Месяц возраста питомца должен быть от "
                f"0 до {Limits.MAX_MONTH_QUANTITY} месяцев"
            )
        return value


class BasePetSerializer(serializers.ModelSerializer):
    """Сериализация питомцев."""

    weight = serializers.DecimalField(
        max_digits=4,
        decimal_places=1,
        required=False,
        default=0,
    )
    age = AgeSerializer(required=True)

    def create(self, validated_data):
        """Создание нового питомца."""
        age_data = validated_data.pop("age")
        age_serializer = AgeSerializer(data=age_data)
        age_serializer.is_valid(raise_exception=True)
        if Age.objects.filter(**age_data).exists():
            age = Age.objects.filter(**age_data).first()
        else:
            age = Age.objects.create(**age_data)
        return Pet.objects.create(age=age, **validated_data)

    def update(self, instance, validated_data):
        """Обновление питомца."""
        age_serializer = AgeSerializer(data=validated_data.get("age"))
        age_serializer.is_valid(raise_exception=True)
        validated_data["age"] = Age.objects.get_or_create(
            **validated_data.get("age")
        )[0]
        instance.age = validated_data["age"]
        return super().update(instance, validated_data)

    class Meta:
        model = Pet
        fields = (
            "name",
            "breed",
            "type",
            "age",
            "weight",
            "owner",
            "is_sterilized",
            "is_vaccinated",
        )


class PetSerializer(BasePetSerializer):
    """Сериализация питомцев с валидацией."""

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_representation(self, instance: Pet) -> dict[str, str | int]:
        """Выносим год и месяц из возраста в основное поле питомца.

        Убираем визуально вложенность.
        """
        representation = super().to_representation(instance)
        age = representation.pop("age")
        representation.update(age)
        return representation

    def to_internal_value(self, data: dict[str, str | int]):
        """Обрабатываем данные питомца..

        Необходимо, чтобы принимать данные, не используя вложенного поля `Age`.
        """
        month = data.pop("month", [])
        year = data.pop("year", [])
        age = AgeSerializer(data={"year": year, "month": month})
        age.is_valid(raise_exception=True)
        data["age"] = age.validated_data
        return super().to_internal_value(data)

    def validate(self, data):
        age = AgeSerializer(data=data.get("age"))
        age.is_valid(raise_exception=True)
        if Pet.objects.filter(
            name=data.get("name"),
            age__year=age.validated_data.get("year"),
            age__month=age.validated_data.get("month"),
            breed=data.get("breed"),
            type=data.get("type"),
        ).exists():
            raise serializers.ValidationError("Такой питомец уже существует!")
        return data
