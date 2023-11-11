import datetime
import re

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.db import models
from rest_framework import serializers

from core.constants import Default, Messages, Limits


def validate_letters(value: str) -> None:
    """
    Проверить, содержит ли данное значение только буквы на русском языке
    или английском.

    Attributes:
        value (str): Значение, которое необходимо проверить.

    Raises:
        ValidationError: Если значение содержит символы, отличные от
        русских или английских букв.

    """
    if not re.match(r"^[a-zA-Zа-яА-Я]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы."
        )


def validate_alphanumeric(value: str) -> None:
    """
    Проверить, содержит ли данное значение только буквы на русском или
    английском языке или цифры.

    Attributes:
        value (str): Значение, которое необходимо проверить.

    Raises:
        ValidationError: Если значение содержит символы, отличные от
        русских или английских букв или цифр.

    """
    if not re.match(r"^[a-zA-Zа-яА-Я0-9\s.,?!()-]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы, цифры, "
            "знаки препинания и скобки."
        )


def validate_cynology_service(service_name: list) -> None:
    """
    Проверяем услуги кинолога на соответствие списку его услуг.

    Args:
        service_name: Имя проверяемой услуги.

    Raises:
        serializers.ValidationError: Если имя_службы отсутствует в списке
        услуг кинолога.

    Returns:
        None.

    """
    if not set(service_name).issubset(set(Default.CYNOLOGY_SERVICES)):
        raise serializers.ValidationError(
            Messages.CYN_SERVICE_ERROR.format(
                service_name=service_name,
                cynology_services=Default.CYNOLOGY_SERVICES,
            )
        )


def validate_cynology_fields(model):
    service_name = model.extra_fields.get("service_name")
    formats = model.extra_fields.get("formats")
    pet_type = model.extra_fields.get("pet_type")
    if not service_name or not formats:
        raise serializers.ValidationError(Messages.CYNOLOGY_FIELDS_ERROR)

    if not set(formats).issubset(set(Default.CYNOLOGY_FORMAT)):
        raise serializers.ValidationError(
            Messages.FORMAT_ERROR.format(
                cynology_format=Default.CYNOLOGY_FORMAT
            )
        )
    if pet_type[0] != Default.PET_TYPE[0][0]:
        raise serializers.ValidationError(
            Messages.PET_TYPE_ERROR,
        )
    if len(pet_type) > 1:
        raise serializers.ValidationError(
            Messages.PET_TYPE_LIST_LENGTH_ERROR,
        )


def validate_vet_service(service_name):
    if not set(service_name).issubset(set(Default.VET_SERVICES)):
        raise serializers.ValidationError(
            Messages.VET_SERVICE_ERROR.format(
                service_name=service_name, vet_services=Default.VET_SERVICES
            )
        )


def validate_vet_fields(model):
    vet_services = model.extra_fields.get("service_name")
    if not vet_services:
        raise serializers.ValidationError(Messages.VET_FIELDS_ERROR)


def validate_grooming_service(service_name: list) -> None:
    """
    Проверяет услугу по уходу за животными, проверяя, находится ли она в
    списке предустановленных типов услуг.

    Attributes:
        service_name: Название услуги по уходу за животными для проверки.

    Raises:
        serializers.ValidationError: Если `service_name` не находится в списке
        предустановленных типов услуг.

    Returns:
        None

    """
    if not set(service_name).issubset(Default.GROOMING_TYPE):
        raise serializers.ValidationError(
            Messages.GROOMING_SERVICE_ERROR.format(
                service_name=service_name, grooming_type=Default.GROOMING_TYPE
            )
        )


def validate_grooming_fields(model):
    grooming_type = model.extra_fields.get("service_name")
    if not grooming_type:
        raise serializers.ValidationError(Messages.GROOMING_FIELDS_ERROR)


def validate_shelter_service(service_name):
    if not set(service_name).issubset(set(Default.SHELTER_SERVICE)):
        raise serializers.ValidationError(
            Messages.SHELTER_SERVICE_ERROR.format(
                service_name=service_name,
                shelter_service=Default.SHELTER_SERVICE,
            )
        )


def validate_shelter_fields(model):
    grooming_type = model.extra_fields.get("grooming_type")
    if grooming_type:
        raise serializers.ValidationError(Messages.GROOMER_FIELDS_ERROR)


def validate_pet_type(model: models.Model) -> None:
    allowed_pet_types = set(pet[0] for pet in Default.PET_TYPE)
    pet_type = model.extra_fields["pet_type"]
    if not set(pet_type).issubset(allowed_pet_types):
        raise serializers.ValidationError(
            {
                "pet_type": f"Тип питомца должен быть одним из: "
                f"{', '.join(allowed_pet_types)}",
            }
        )


class RangeValueValidator(BaseValidator):
    def __init__(self, value_from, value_to):
        self.value_from = value_from
        self.value_to = value_to

    def __call__(self, value):
        if not self.value_from <= int(value) <= self.value_to:
            raise ValidationError(
                f"Значение {value} должно быть в пределах от {self.value_from}"
                f" до {self.value_to}"
            )


def validate_current_and_future_month(value):
    current_month = datetime.date.today().month
    if value.month < current_month or value.month > current_month + 1:
        raise ValidationError(
            "Дата должна быть в текущем или следующем месяце."
        )


def validate_working_hours(value):
    if len(value) != 2:
        raise ValidationError("Рабочие часы должны быть в корректном формате")
    if value[1] <= value[0]:
        raise ValidationError("Конечное время должно быть больше начального.")


def validate_age(value):
    if value[0] < Limits.MIN_AGE_PET or value[0] > Limits.MAX_AGE_PET:
        raise ValidationError(
            f"Возраст питомца должен быть от {Limits.MIN_AGE_PET} до "
            f"{Limits.MAX_AGE_PET} лет"
        )

    if value[1] < 0 or value[1] > 12:
        raise ValidationError(f"Количество месяцев долджно быть от 0 до 12.")


class PhoneNumberValidator(BaseValidator):
    def __init__(self, value_from, value_to):
        self.value_from = value_from
        self.value_to = value_to

    def __call__(self, value):
        if not re.match(r"^8\d{10}$", value):
            raise ValidationError(
                "Номер телефона должен быть в формате 89999999999"
            )


def validate_price(attrs):
    if attrs["cost_from"] > attrs["cost_to"]:
        raise serializers.ValidationError(
            "`cost_from` не может быть больше `cost_to`"
        )
    return attrs


def validate_schedule(attrs):
    start_work_time = attrs.get("start_work_time")
    end_work_time = attrs.get("end_work_time")
    break_start_time = attrs.get("break_start_time")
    break_end_time = attrs.get("break_end_time")

    if start_work_time > end_work_time:
        raise serializers.ValidationError(
            "`start_work_time` не может быть больше `end_work_time`"
        )
    if break_start_time > break_end_time:
        raise serializers.ValidationError(
            "`break_start_time` не может быть больше `break_end_time`"
        )
    if start_work_time > break_start_time:
        raise serializers.ValidationError(
            "`start_work_time` не может быть больше `break_start_time`"
        )
    if break_end_time > end_work_time:
        raise serializers.ValidationError(
            "`break_end_time` не может быть больше `end_work_time`"
        )

    return attrs
