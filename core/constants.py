from datetime import timedelta


class Limits:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    MIN_AGE_PET = 0
    MIN_DURATION = 1
    MIN_PRICE = 1
    MIN_LEN_PHONE_NUMBER = 10

    MAX_LEN_TITLE_NAME = 50
    MAX_LEN_SERVICE_NAME = 50
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
    CYN_SERVICE_ERROR = ("У кинолога нет такой услуги: {service_name}. "
                         "Выбор из услуг: {cynology_services}")
    VET_SERVICE_ERROR = ("У ветеринара нет такой услуги: {service_name}. "
                         "Выбор из услуг: {vet_services}")
    GROOMING_SERVICE_ERROR = ("У грумера нет такой услуги: {service_name}. "
                              "Выбор из услуг: {grooming_type}")
    SHELTER_SERVICE_ERROR = ("У зооняни нет такой услуги: {service_name}. "
                             "Зооняня не предлает других услуг, кроме "
                             "{shelter_service}.")
    CYNOLOGY_FIELDS_ERROR = "Поля service_name и format необходимо заполнить."
    VET_FIELDS_ERROR = "Поле service_name необходимо заполнить."
    GROOMING_FIELDS_ERROR = "Поле grooming_type необходимо заполнить."
    GROOMER_FIELDS_ERROR = "Поле grooming_type только для Грумера."
    CLEANUP_FIELDS_ERROR = "Поля service_name и formats только для Кинолога."
    SERVICE_NAME_ERROR = ("Поле service_name должно быть из списка услуг: "
                          "{cynology_services}")
    FORMAT_ERROR = "Поле format должно быть из списка услуг: {cynology_format}"
    PET_TYPE_ERROR = "Кинолог работает только с собаками"
    PET_TYPE_LIST_LENGTH_ERROR = "Длина списка питомцев должна быть равна 1."
class Default:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")
    COST_FROM = 500
    COST_TO = 1000
    PET_AGE = 1
    WEIGHT_CHOICES = (
        ("1", "до 5кг."),
        ("2", "5 - 10кг."),
        ("3", "10 - 20кг."),
        ("4", "более 20кг."),
    )

    VET_SERVICES = (
        "consultation",
        "veterinary",
        "injection",
        "vaccinating",
        "sterializing",
        "vetpassport",
        "sleeping",
        "another",
    )
    
    SERVICES = (
        ("cynology", "Кинолог" ),
        ("veterenary", "Ветеринар" ),
        ("shelter", "Зооняня" ),
        ("grooming", "Грумер"),
    )
    
    CYNOLOGY_SERVICES = (
        "Коррекция проблемного поведения",
        "Воспитательная дрессировка щенка",
        "Обучение командам",
        "Дрессировка служебных/ охотничьих собак, подготовка к экзамену ОКД",
        "Спортивная дрессировка",
        "Адаптация собаки из приюта",
        "Подготовка к участию на выставке",
        "Консультация",
        "Другое",
    )
    
    CYNOLOGY_FORMAT = (
        "individual",
        "minigroup",
        "group",
        "training",
        "another",
    )
    
    GROOMING_TYPE = (
        "Hygienic",
        "Exhibition",
        "Decorative",
        "ych",
    )
    SHELTER_SERVICE = ["shelter"]
    SERVICER_PRICE = [1000, 2000]
    PET_TYPE = (
        ("dog", "Собака"),
        ("cat", "Кошка"),
        ("pig", "Морская свинка"),
        ("hom", "Хомяк"),
        ("hor", "Хорек"),
        ("rab", "Кролик"),
        ("ano", "Другое"),
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

    DAYS_OF_WEEK = (
        ("Пн.", "Понедельник"),
        ("Вт.", "Вторник"),
        ("Ср.", "Среда"),
        ("Чт", "Четверг"),
        ("Пт.", "Пятница"),
        ("Сб.", "Суббота"),
        ("Вс.", "Воскресенье"),
    )
    TIME_PER_VISIT_CHOICES = ((0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0))
    GOODS_IMAGE_SIZE = 500, 300

