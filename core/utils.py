from core.constants import Default


def grooming_type_default():
    """Вспомогательная функция для определения значения по умолчанию
    в поле ArrayField.
    """
    return Default.GROOMING_TYPE[0]


def cynology_type_default():
    """Вспомогательная функция для определения значения по умолчанию
    в поле ArrayField.
    """
    return Default.SYNOLOGY_TASKS[0]
