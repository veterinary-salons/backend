import re

from django.core.exceptions import ValidationError

from core.constants import Default


def validate_letters(value):
    if not re.match(r"^[a-zA-Zа-яА-Я]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы."
        )


def validate_alphanumeric(value):
    if not re.match(r"^[a-zA-Zа-яА-Я0-9\s.-,?!()]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы, цифры, "
            "знаки препинания и скобки."
        )

def validate_services(name, pet_type, task, formats, grooming_type):
    print(name)
    if name == Default.SERVICES[0][0] and pet_type != "dog":
        print(task, formats)
        raise ValidationError("Кинолог работает только с собаками.")
    if name != Default.SERVICES[0][0] and any(
        (
            task,
            formats,
        )
    ):
        raise ValidationError("Поля `task` и `formats` только для Кинолога.")
    if name != Default.SERVICES[3][0] and grooming_type:
        raise ValidationError("Поле `grooming_type` только для Грумера.")
    if name == Default.SERVICES[3][0] and not grooming_type:
        raise ValidationError("Поле `grooming_type` необходимо заполнить.")
    if name == Default.SERVICES[0][0] and not all(
        (
            task,
            formats,
        )
    ):
        raise ValidationError("Поле `task` и `formats` необходимо заполнить.")
