class Limits:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    MAX_LEN_ANIMAL_TYPE = 30
    MAX_LEN_ANIMAL_BREED = 30
    MAX_LEN_ANIMAL_NAME = 50

    # Возраст пока в годах, потом можно подумать...
    MIN_AGE_PET = 0
    MAX_AGE_PET = 50
    MIN_DURATION = 1
    MAX_DURATION = 600
    MAX_LENGTH_ABOUT = 300
    PLACE_MAX_LENGTH = 300

class MESSAGES:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    CORRECT_AGE_MESSAGE = "Введите корректный возраст!"


class DEFAULT:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    PET_AGE = 1
    WEIGHT_CHOICES = (
        ("1", "до 5кг."),
        ("2", "5 - 10кг."),
        ("3", "10 - 20кг."),
        ("4", "более 20кг."),
    )
    GROOMING_TYPE = (
        ("h", "Hygienic"),
        ("e", "Exhibition"),
        ("d", "Decorative"),
        ("y", "You can choose"),
    )
    SYNOLOGY_TASKS = (
        ("c", "Коррекция проблемного поведения"),
        ("l", "Воспитательная дрессировка щенка"),
        ("t", "Обучение командам"),
        (
            "d",
            "Дрессировка служебных/ охотничьих собак, подготовка "
            "к экзамену ОКД",
        ),
        ("s", "Спортивная дрессировка"),
        ("a", "Адаптация собаки из приюта"),
        ("b", "Подготовка к участию на выставке"),
        ("k", "Консультация"),
        ("n", "Другое"),
    )
    SYNOLOGY_FORMAT = (
        ("i", "Индивидуальные занятия"),
        ("m", "Занятия в мини-группе"),
        ("g", "Групповые занятия"),
        ("d", "Дрессировка с передержкой у кинолога"),
        ("n", "Другое"),
    )
    SERVICER_PRICE = 500
    PET_TYPE = (
        ("cat", "Кошка"),
        ("dog", "Собака"),
        ("pig", "Морская свинка"),
        ("hom", "Хомяк"),
        ("ano", "Другое"),
    )

