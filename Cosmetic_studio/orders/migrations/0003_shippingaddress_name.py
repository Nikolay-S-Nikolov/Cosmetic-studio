# Generated by Django 5.1.2 on 2024-12-01 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='name',
            field=models.CharField(default='Noname', max_length=50),
            preserve_default=False,
        ),
    ]
