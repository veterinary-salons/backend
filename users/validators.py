import re

from django.core.exceptions import ValidationError


def phone_number_validator(value):
    if value[0] == "+":
        value = value[1:]
    if not value.isdecimal():
        raise ValidationError("Phone number must only contain decimal digits")
