import re

from django.core.exceptions import ValidationError


def validate_letters(value):
    if not re.match(r"^[a-zA-Zа-яА-Я]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы."
        )


def validate_alphanumeric(value):
    if not re.match(r"^[a-zA-Zа-яА-Я0-9\s.,?!()]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы, цифры, "
            "знаки препинания и скобки."
        )

def validate_service_name(value):
    if not re.match(r"^[а-яА-Я -.,]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские буквы, пробел, дефис, "
            "точки и запятые."
        )