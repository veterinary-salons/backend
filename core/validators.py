import datetime
import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, BaseValidator
from icecream import ic
from rest_framework import serializers

from core.constants import Default, Messages, Limits


def validate_letters(value):
    if not re.match(r"^[a-zA-Zа-яА-Я]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы."
        )


def validate_alphanumeric(value):
    if not re.match(r"^[a-zA-Zа-яА-Я0-9\s.,?!()-]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы, цифры, "
            "знаки препинания и скобки."
        )


def validate_cynology_service(service_name):
    if service_name not in Default.CYNOLOGY_SERVICES:
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

    if formats not in Default.CYNOLOGY_FORMAT:
        raise serializers.ValidationError(
            Messages.FORMAT_ERROR.format(
                cynology_format=Default.CYNOLOGY_FORMAT
            )
        )

    if pet_type != Default.PET_TYPE[0][0]:
        raise serializers.ValidationError(
            Messages.PET_TYPE_ERROR,
        )


def validate_vet_service(service_name):
    if service_name not in Default.VET_SERVICES:
        raise serializers.ValidationError(
            Messages.VET_SERVICE_ERROR.format(
                service_name=service_name, vet_services=Default.VET_SERVICES
            )
        )


def validate_vet_fields(model):
    vet_services = model.extra_fields.get("vet_services")
    if not vet_services:
        raise serializers.ValidationError(Messages.VET_FIELDS_ERROR)


def validate_grooming_service(service_name):
    if service_name not in Default.GROOMING_TYPE:
        raise serializers.ValidationError(
            Messages.GROOMING_SERVICE_ERROR.format(
                service_name=service_name, grooming_type=Default.GROOMING_TYPE
            )
        )


def validate_grooming_fields(model):
    grooming_type = model.extra_fields.get("grooming_type")
    if not grooming_type:
        raise serializers.ValidationError(Messages.GROOMING_FIELDS_ERROR)


def validate_shelter_service(service_name):
    if service_name != Default.SHELTER_SERVICE:
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


# def validate_extra_fields(model: Service) -> None:
#     specialist_type = model.category
#     service_name = model.extra_fields.get("service_name")
#
#     if specialist_type == Default.SERVICES[0][0]:
#         validate_cynology_service(service_name)
#         validate_cynology_fields(model)
#     elif specialist_type == Default.SERVICES[1][0]:
#         validate_vet_service(service_name)
#         validate_vet_fields(model)
#     elif specialist_type == Default.SERVICES[2][0]:
#         validate_grooming_service(service_name)
#         validate_grooming_fields(model)
#     elif specialist_type == Default.SERVICES[3][0]:
#         validate_shelter_service(service_name)
#         validate_shelter_fields(model)


class RangeValueValidator(BaseValidator):
    def __init__(self, value_from, value_to):
        self.value_from = value_from
        self.value_to = value_to

    def __call__(self, value):
        if not self.value_from < int(value) < self.value_to:
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


#
# def validate_cost(value):
#     if not isinstance(value, dict) or len(value) != 2:
#         raise ValidationError(
#             "Поле cost должно содержать ровно две пары значений.",
#             params={"value": value},
#         )
