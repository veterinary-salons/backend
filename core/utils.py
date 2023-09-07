from core.constants import DEFAULT


def grooming_type_default():
    """Вспомогательная функция для определения значения по умолчанию
    в поле ArrayField.
    """
    return DEFAULT.GROOMING_TYPE[0]


def synology_type_default():
    """Вспомогательная функция для определения значения по умолчанию
    в поле ArrayField.
    """
    return DEFAULT.SYNOLOGY_TASKS[0]
