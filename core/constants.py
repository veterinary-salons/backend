from datetime import timedelta


class Limits:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    MIN_AGE_PET = 0
    MIN_DURATION = 1
    MIN_PRICE = 1
    MIN_LEN_PHONE_NUMBER = 10

    MAX_LEN_SERVICE_NAME = 20
    MAX_LEN_SERVICE_TYPE = 30
    MAX_LEN_ANIMAL_TYPE = 30
    MAX_LEN_ANIMAL_BREED = 30
    MAX_LEN_ANIMAL_NAME = 30
    MAX_LEN_CATEGORY_NAME = 30
    MAX_LEN_GOODS_NAME = 200
    MAX_LEN_BRAND_NAME = 50
    MAX_AGE_PET = 50
    MAX_DURATION = 650
    MAX_LEN_ABOUT = 300
    MAX_PLACE_LENGTH = 300
    MAX_PRICE = 100000
    MAX_LEN_PHONE_NUMBER = 12
    MAX_LEN_EMAIL = 50
    MAX_LEN_ADDRESS = 100
    MAX_MONTH_QUANTITY = 11

    CONFIRMATION_CODE_LENGTH = 5

    RECOVERY_ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)
    EMAIL_CODE_LIFETIME = timedelta(minutes=10)


class Messages:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    CORRECT_AGE_MESSAGE = "Введите корректный возраст!"
    CORRECT_PRICE_MESSAGE = "Введите корректную цену."
    CORRECT_DURATION_MESSAGE = "Некорректная продолжительность."

class Default:
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
        ("Hygienic", "Hygienic"),
        ("Exhibition", "Exhibition"),
        ("Decorative", "Decorative"),
        ("ych", "You can choose"),
    )
    CYNOLOGY_SERVICES = (
        ("correction", "Коррекция проблемного поведения"),
        ("etraining", "Воспитательная дрессировка щенка"),
        ("education", "Обучение командам"),
        (
            "training",
            "Дрессировка служебных/ охотничьих собак, подготовка "
            "к экзамену ОКД",
        ),
        ("sport", "Спортивная дрессировка"),
        ("adapt", "Адаптация собаки из приюта"),
        ("prep", "Подготовка к участию на выставке"),
        ("consult", "Консультация"),
        ("another", "Другое"),
    )
    CYNOLOGY_FORMAT = (
        ("individual", "Индивидуальные занятия"),
        ("minigroup", "Занятия в мини-группе"),
        ("group", "Групповые занятия"),
        ("training", "Дрессировка с передержкой у кинолога"),
        ("another", "Другое"),
    )
    SERVICER_PRICE = [1000, 2000]
    PET_TYPE = (
        ("cat", "Кошка"),
        ("dog", "Собака"),
        ("pig", "Морская свинка"),
        ("hom", "Хомяк"),
        ("hor", "Хорек"),
        ("rab", "Кролик"),
        ("ano", "Другое"),
    )
    SERVICES = (
        ("cynology", "Кинолог" ),
        ("veterenary", "Ветеринар" ),
        ("shelter", "Зооняня" ),
        ("grooming", "Грумер"),
    )
    GOODS_CATEGORIES = (
        ("food", "Корм и лакомства"),
        ("toys", "Игрушки и амуниция"),
        ("toilet", "Для туалета"),
        ("hygiene", "Гигиена и уход"),
        ("bowls", "Миски, лежанки, домики"),
        ("vetaptheca", "Ветаптека"),
    )
    AGE_CHOICES = (
        ('any', 'For any age'),
        ('0-11', '0-1'),
        ('1-3', '1-3'),
        ('4-10', '4-10'),
        ('11-20', '11-20'),
        ('21-30', '21-30'),
    )
    VET_SERVICES=(
        ("consultation", "Консультации"),
        ("veterinary", "Диагностика заболевания и лечение"),
        ("injection", "Введение инъекций"),
        ("vaccinating", "Вакцинация"),
        ("sterializing", "Стерилизация"),
        ("vetpassport", "Оформление ветпаспорта"),
        ("sleeping", "Усыпление"),
        ("another", "Другое"),
    )
    DAYS_OF_WEEK = (
        (0, "Понедельник"),
        (1, "Вторник"),
        (2, "Среда"),
        (3, "Четверг"),
        (4, "Пятница"),
        (5, "Суббота"),
        (6, "Воскресенье"),
    )
    GOODS_IMAGE_SIZE = 500, 300

