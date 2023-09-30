# Generated by Django 4.2.4 on 2023-09-30 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierprofile',
            name='serve_at_customer',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplierprofile',
            name='serve_at_supplier',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
    ]
