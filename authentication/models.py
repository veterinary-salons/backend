from random import choices as random_choices
from string import digits

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.timezone import now as timezone_now

from core.constants import Limits


User = get_user_model()


def create_code():
    return "".join(random_choices(digits, k=5))

class EmailCode(models.Model):
    email = models.EmailField(
        unique=True,
        max_length=Limits.MAX_LEN_EMAIL,
    )
    code = models.CharField(
        max_length=5,
        validators=(MinLengthValidator(5),),
        default=create_code,
    )
    created_at = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    lifetime = Limits.EMAIL_CODE_LIFETIME

    @property
    def is_valid(self):
        return timezone_now() <  (self.created_at + self.lifetime)

    def update_code(self):
        self.code = create_code()
        self.confirmed = False
        self.save()

    def confirm(self):
        self.confirmed = True
        self.code = create_code()
        self.save()
