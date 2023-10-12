# Generated by Django 4.2.4 on 2023-10-12 19:35

import core.utils
import core.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[core.validators.validate_alphanumeric], verbose_name='название услуги')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('to_date', models.DateTimeField(default=django.utils.timezone.now, validators=[core.validators.validate_current_and_future_month])),
                ('place', models.CharField(blank=True, max_length=300, null=True, validators=[core.validators.validate_alphanumeric])),
                ('is_done', models.BooleanField(default=False, verbose_name='подтверждено или нет')),
                ('actual', models.BooleanField(default=False, verbose_name='активно или нет')),
                ('customer_place', models.BooleanField(default=False)),
                ('supplier_place', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'бронь услуги',
                'verbose_name_plural': 'брони услуг',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday_hours', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
                ('tuesday_hours', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
                ('wednesday_hours', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
                ('thursday_hours', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
                ('friday_hours', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
                ('saturday_hours', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
                ('sunday_hours', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
                ('breakTime', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[core.validators.RangeValueValidator(0, 24)]), null=True, size=2)),
            ],
            options={
                'verbose_name': 'расписание специалиста',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[core.validators.validate_alphanumeric], verbose_name='название услуги')),
                ('pet_type', models.CharField(choices=[('cat', 'Кошка'), ('dog', 'Собака'), ('pig', 'Морская свинка'), ('hom', 'Хомяк'), ('hor', 'Хорек'), ('rab', 'Кролик'), ('ano', 'Другое')], max_length=30, verbose_name='тип животного')),
                ('specialist_type', models.CharField(blank=True, choices=[('cynology', 'Кинолог'), ('veterenary', 'Ветеринар'), ('shelter', 'Зооняня'), ('grooming', 'Грумер')], max_length=30, null=True, validators=[core.validators.validate_letters], verbose_name='тип услуги')),
                ('price', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(validators=[core.validators.RangeValueValidator(1, 100000)]), default=core.utils.default_price, size=None)),
                ('description', models.TextField(blank=True, max_length=300, null=True, validators=[core.validators.validate_alphanumeric], verbose_name='О себе')),
                ('published', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_services', to='services.booking')),
                ('schedule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.schedule')),
            ],
            options={
                'verbose_name': 'услуга',
                'verbose_name_plural': 'услуги',
            },
        ),
    ]
