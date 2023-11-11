# Generated by Django 4.2.4 on 2023-11-11 13:20

import core.utils
import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(max_length=1000)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "to_date",
                    models.DateTimeField(
                        default=core.utils.default_booking_time,
                        validators=[core.validators.validate_current_and_future_month],
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="активно или нет"),
                ),
                (
                    "is_confirmed",
                    models.BooleanField(
                        default=False, verbose_name="подтверждено или нет"
                    ),
                ),
                (
                    "is_done",
                    models.BooleanField(default=False, verbose_name="окончено или нет"),
                ),
                (
                    "is_cancelled",
                    models.BooleanField(default=False, verbose_name="отменено или нет"),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="users.customerprofile",
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "бронь услуги",
                "verbose_name_plural": "брони услуг",
            },
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ad_title",
                    models.CharField(
                        max_length=50,
                        validators=[core.validators.validate_alphanumeric],
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("cynology", "Кинолог"),
                            ("veterenary", "Ветеринар"),
                            ("shelter", "Зооняня"),
                            ("grooming", "Грумер"),
                        ],
                        max_length=30,
                        validators=[core.validators.validate_letters],
                        verbose_name="тип услуги",
                    ),
                ),
                ("description", models.CharField(max_length=50)),
                ("customer_place", models.BooleanField(default=False)),
                ("supplier_place", models.BooleanField(default=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="images")),
                ("extra_fields", models.JSONField()),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="users.supplierprofile",
                        verbose_name="исполнитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "услуга",
                "verbose_name_plural": "услуги",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=500)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[core.validators.RangeValueValidator(1, 5)]
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="users.customerprofile",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="services.service",
                    ),
                ),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы",
            },
        ),
        migrations.CreateModel(
            name="Price",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("service_name", models.CharField(max_length=50)),
                (
                    "cost_from",
                    models.DecimalField(
                        decimal_places=0,
                        default=500,
                        max_digits=5,
                        validators=[core.validators.RangeValueValidator(1, 100000)],
                    ),
                ),
                (
                    "cost_to",
                    models.DecimalField(
                        decimal_places=0,
                        default=1000,
                        max_digits=5,
                        validators=[core.validators.RangeValueValidator(1, 100000)],
                    ),
                ),
                (
                    "customer",
                    models.ManyToManyField(
                        related_name="prices",
                        through="services.Booking",
                        to="users.customerprofile",
                        verbose_name="клиенты",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="services.service",
                    ),
                ),
            ],
            options={
                "verbose_name": "стоимость услуги",
                "verbose_name_plural": "стоимости услуг",
            },
        ),
        migrations.CreateModel(
            name="FavoriteArticles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "article_id",
                    models.PositiveIntegerField(
                        validators=[core.validators.RangeValueValidator(1, 6)]
                    ),
                ),
                (
                    "date_added",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата добавления"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_articles",
                        to="users.customerprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "избранные статьи",
                "verbose_name_plural": "избранные статьи",
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_added",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата добавления"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="in_favorites",
                        to="users.customerprofile",
                        verbose_name="заказчик",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="in_favorites",
                        to="services.service",
                        verbose_name="понравившиеся услуги",
                    ),
                ),
            ],
            options={
                "verbose_name": "избранная услуга",
                "verbose_name_plural": "избранные услуги",
            },
        ),
        migrations.AddField(
            model_name="booking",
            name="price",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="services.price",
            ),
        ),
        migrations.AddConstraint(
            model_name="price",
            constraint=models.CheckConstraint(
                check=models.Q(("cost_from__lte", models.F("cost_to"))),
                name="cost_range",
            ),
        ),
    ]
