# Generated by Django 4.2.4 on 2023-10-08 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='users.customerprofile', verbose_name='владелец питомца'),
        ),
        migrations.AddConstraint(
            model_name='pet',
            constraint=models.UniqueConstraint(fields=('name', 'breed', 'age', 'type'), name='unique_name_for_pet'),
        ),
    ]
