# Generated by Django 4.2.4 on 2023-09-30 20:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_supplierprofile_serve_at_customer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('cat', 'Кошка'), ('dog', 'Собака'), ('pig', 'Морская свинка'), ('hom', 'Хомяк'), ('ano', 'Другое')], max_length=30, verbose_name='вид животного')),
                ('breed', models.CharField(max_length=30, verbose_name='порода')),
                ('name', models.CharField(max_length=30, verbose_name='имя питомца')),
                ('age', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, 'Введите корректный возраст!'), django.core.validators.MaxValueValidator(50, 'Введите корректный возраст!')], verbose_name='Возраст питомца')),
                ('weight', models.CharField(choices=[('1', 'до 5кг.'), ('2', '5 - 10кг.'), ('3', '10 - 20кг.'), ('4', 'более 20кг.')], max_length=10)),
                ('is_sterilized', models.BooleanField(default=False)),
                ('is_vaccinated', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='users.customerprofile', verbose_name='владелец питомца')),
            ],
            options={
                'verbose_name': 'питомец',
                'verbose_name_plural': 'питомцы',
                'ordering': ('name',),
            },
        ),
        migrations.AddConstraint(
            model_name='pet',
            constraint=models.UniqueConstraint(fields=('name', 'breed', 'type', 'age', 'owner'), name='unique_for_pet'),
        ),
    ]
