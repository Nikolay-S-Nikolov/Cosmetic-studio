# Generated by Django 5.1.2 on 2024-12-01 15:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_shippingaddress_email_shippingaddress_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Please, enter a valid phone number in the format 0888123456', regex='^0\\d{9}$')]),
        ),
    ]
