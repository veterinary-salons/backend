from datetime import timedelta


class Limits:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    MIN_RATING = 1
    MIN_AGE_PET = 0
    MIN_DURATION = 1
    MIN_PRICE = 1
    MIN_LEN_PHONE_NUMBER = 10

    MAX_ARTICLE_ID_NUMBER = 6
    MAX_LEN_ADDRESS = 300
    MAX_LEN_CUSTOMER_NAME = 20
    MAX_LEN_TITLE_NAME = 50
    MAX_LEN_SERVICE_NAME = 50
    MAX_LEN_SERVICE_TYPE = 30
    MAX_LEN_ANIMAL_TYPE = 30
    MAX_LEN_ANIMAL_BREED = 30
    MAX_LEN_ANIMAL_NAME = 30
    MAX_LEN_CATEGORY_NAME = 30
    MAX_LEN_DESCRIPTION = 1000
    MAX_LEN_GOODS_NAME = 200
    MAX_LEN_BRAND_NAME = 50
    MAX_LEN_REVIEW = 500
    MAX_AGE_PET = 50
    MAX_DURATION = 650
    MAX_LEN_ABOUT = 300
    MAX_PLACE_LENGTH = 300
    MAX_PRICE = 100000
    MAX_LEN_PHONE_NUMBER = 12
    MAX_LEN_EMAIL = 50
    MAX_MONTH_QUANTITY = 11
    MAX_CHOICE_LENGTH = 10
    MAX_RATING = 5
    CONFIRMATION_CODE_LENGTH = 5

    RECOVERY_ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)
    EMAIL_CODE_LIFETIME = timedelta(minutes=10)


class Messages:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"can't reassign constant '{name}'")

    CORRECT_AGE_MESSAGE = "Введите корректный возраст!"
    CORRECT_PRICE_MESSAGE = "Введите корректную цену."
    CORRECT_DURATION_MESSAGE = "Некорректная продолжительность."
    CYN_SERVICE_ERROR = (
        "У кинолога нет такой услуги: {service_name}. "
        "Выбор из услуг: {cynology_services}"
    )
    VET_SERVICE_ERROR = (
        "У ветеринара нет такой услуги: {service_name}. "
        "Выбор из услуг: {vet_services}"
    )
    GROOMING_SERVICE_ERROR = (
        "У грумера нет такой услуги: {service_name}. "
        "Выбор из услуг: {grooming_type}"
    )
    SHELTER_SERVICE_ERROR = (
        "У зооняни нет такой услуги: {service_name}. "
        "Зооняня не предлает других услуг, кроме "
        "{shelter_service}."
    )
    CYNOLOGY_FIELDS_ERROR = (
        "Поля service_name, format и pet_type необходимо заполнить."
    )
    VET_FIELDS_ERROR = "Поля `service_name` и `pet_type` необходимо заполнить."
    CYNOLOGY_NUM_FIELDS_ERROR = "У кинолога должно быть 3 поля `service_name`, `pet_type`, `study_format`"
    GROOMER_FIELDS_ERROR = (
        "У грумера должно быть 2 поля `service_name`, `pet_type`"
    )
    VET_NUM_FIELDS_ERROR = (
        "У ветеринара должно быть 2 поля `service_name`, `pet_type`"
    )
    SHELTER_NUM_FIELDS_ERROR = (
        "У зооняни должно быть только 1 поле `service_name`"
    )
    CLEANUP_FIELDS_ERROR = "Поля service_name и formats только для Кинолога."
    SERVICE_NAME_ERROR = (
        "Поле service_name должно быть из списка услуг: " "{cynology_services}"
    )
    FORMAT_ERROR = "Поле format должно быть из списка услуг: {cynology_format}"
    PET_TYPE_ERROR = "Кинолог работает только с собаками"
    NO_PET_TYE_ERROR = "Поле `pet_type` необходимо заполнить."
    PET_TYPE_LIST_LENGTH_ERROR = "Длина списка питомцев должна быть равна 1."


class Default:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(
            f" Нельзя переопределить название константы '{name}'"
        )

    PATH_TO_AVATAR_ADVERTISEMENT = "users/suppliers/advertisement/"
    PATH_TO_AVATAR_CUSTOMER = "users/customers/avatar/"
    PATH_TO_AVATAR_SUPPLIER = "users/suppliers/avatar/"
    PATH_TO_AVATAR_PET = "pets/avatar/"
    PROTOCOL = "http://"
    COST_FROM = 500
    COST_TO = 1000
    PET_AGE = 1
    STERILIZED_CHOICES = (
        ("Да", "Стерилизован"),
        ("Нет", "Не стерилизован"),
        ("Не знаю", "Не знаю"),
    )
    VACCINATED_CHOICES = (
        ("Да", "Вакцинирован"),
        ("Нет", "Не вакцинирован"),
        ("Не знаю", "Не знаю"),
    )
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
        ("cynology", "Кинолог"),
        ("veterenary", "Ветеринар"),
        ("shelter", "Зооняня"),
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
        "Индивидуальный",
        "Минигруппы",
        "Групповой",
        "Тренировочный",
        "Другой",
    )

    GROOMING_TYPE = (
        "Гигиенический",
        "Выставочный",
        "Декоративный",
    )
    SHELTER_SERVICE = [
        "shelter",
    ]
    SERVICER_PRICE = [1000, 2000]

    PET_TYPE = [
        (pet, pet)
        for pet in (
            "Собака",
            "Кошка",
            "Морская свинка",
            "Хомяк",
            "Хорек",
            "Кролик",
            "Другое",
        )
    ]

    GOODS_CATEGORIES = (
        ("food", "Корм и лакомства"),
        ("toys", "Игрушки и амуниция"),
        ("toilet", "Для туалета"),
        ("hygiene", "Гигиена и уход"),
        ("bowls", "Миски, лежанки, домики"),
        ("vetaptheca", "Ветаптека"),
    )
    AGE_CHOICES = (
        ("any", "For any age"),
        ("0-11", "0-1"),
        ("1-3", "1-3"),
        ("4-10", "4-10"),
        ("11-20", "11-20"),
        ("21-30", "21-30"),
    )

    DAYS_OF_WEEK = (
        ("Пн", "Понедельник"),
        ("Вт", "Вторник"),
        ("Ср", "Среда"),
        ("Чт", "Четверг"),
        ("Пт", "Пятница"),
        ("Сб", "Суббота"),
        ("Вс", "Воскресенье"),
    )
    DAYS_NUMBER = {
        0: "Пн",
        1: "Вт",
        2: "Ср",
        3: "Чт",
        4: "Пт",
        5: "Сб",
        6: "Вс",
    }

    TIME_PER_VISIT_CHOICES = (
        (30, "0.5 часа"),
        (60, "1 час"),
        (90, "1.5 часа"),
        (120, "2 часа"),
    )
    GOODS_IMAGE_SIZE = 500, 300
