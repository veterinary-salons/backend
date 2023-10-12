from django.db import models

class YesNoDontKnow(models.TextChoices):
    YES = "Да", "Да"
    NO = "Нет", "Нет"
    DONT_KNOW = "Не знаю", "Не знаю"
