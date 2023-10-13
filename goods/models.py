from PIL import Image
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from core.constants import Limits, Default, Messages
from pets.models import Animal
from users.models import CustomerProfile

User = get_user_model()

class GoodsCategory(models.Model):
    """Класс категории товаров."""

    name = models.CharField(
        max_length=Limits.MAX_LEN_CATEGORY_NAME,
        choices=Default.GOODS_CATEGORIES,
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self) -> str:
        return self.name


class Goods(models.Model):
    """Класс товара."""

    name = models.CharField(
        max_length=Limits.MAX_LEN_GOODS_NAME,
    )
    animal_type = models.ForeignKey(Animal, on_delete=models.CASCADE)
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE)
    age = models.CharField(max_length=10, choices=Default.AGE_CHOICES)
    brand = models.CharField(max_length=Limits.MAX_LEN_BRAND_NAME)
    price = models.DecimalField(
        max_digits=7, decimal_places=2,
        validators=(
            MinValueValidator(
                Limits.MIN_PRICE,
                Messages.CORRECT_PRICE_MESSAGE,
            ),
            MaxValueValidator(
                Limits.MAX_PRICE,
                Messages.CORRECT_PRICE_MESSAGE,
            ),
        ),
    )
    image = models.ImageField(upload_to='images/goods/', blank=True, null=True)
    def save(self, *args, **kwargs) -> None:
        """Изменяет формат изображения при сохранении товара."""

        super().save(*args, **kwargs)
        image = Image.open(self.image.path)
        image = image.resize(Default.GOODS_IMAGE_SIZE)
        image.save(self.image.path)

    def delete(self, *args, **kwargs):
        """Удаляет изображение при удалении товара."""

        self.image.delete()
        super().delete(*args, **kwargs)

class Favorite(models.Model):
    """Избранные товары.

    Модель связывает Goods и User.

    """

    goods = models.ForeignKey(
        Goods,
        verbose_name='понравившиеся товары',
        related_name='in_favorites',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomerProfile,
        verbose_name='пользователь',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='дата добавления',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'избранный товар'
        verbose_name_plural = 'избранные товары'
        constraints = (
            UniqueConstraint(
                fields=(
                    'goods',
                    'user',
                ),
                name='%(app_label)s_%(class)s товар уже в избранном',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.goods}'



class Cart(models.Model):
    """Товары в корзине покупок.

    Модель связывает Recipe и  User.

    """
    goods = models.ForeignKey(
        Goods,
        verbose_name='товары в списке покупок',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='владелец списка',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'товар в списке покупок'
        verbose_name_plural = 'товары в списке покупок'
        constraints = (
            UniqueConstraint(
                fields=(
                    'goods',
                    'user',
                ),
                name='%(app_label)s_%(class)s товар уже в корзине',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} добавил в корзину {self.goods}'
