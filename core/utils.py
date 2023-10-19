from core.constants import Default


def grooming_type_default():
    """Вспомогательная функция для определения значения по умолчанию
    в поле ArrayField.
    """
    return Default.GROOMING_TYPE[0]


def default_price():
    """Вспомогательная функция для определения значения по умолчанию
    в поле ArrayField.
    """
    return Default.SERVICER_PRICE


def remove_dict_fields(dictionary: dict[str,], fields: list[str,]) -> dict:
    """
    Удаляет указанные ключи из словаря.

    Args:
        dictionary (dict): Словарь, из которого нужно удалить ключи.
        fields (list): Список ключей, которые нужно удалить.

    Returns:
        dict: Измененный словарь без указанных ключей.

    """
    for field in fields:
        dictionary.pop(field, None)
    return dictionary

def service_choice(specialist_type):
    if specialist_type == Default.SERVICES[0][0]:
        return Default.CYNOLOGY_SERVICES
    
    elif specialist_type == Default.SERVICES[1][0]:
        return Default.VET_SERVICES
    
    elif specialist_type == Default.SERVICES[2][0]:
        return []
    
    elif specialist_type == Default.SERVICES[3][0]:
        return Default.GROOMING_TYPE
