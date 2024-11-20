# Generated by Django 5.1.2 on 2024-11-20 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_preferred_name_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='preferred_name_nickname',
            field=models.CharField(blank=True, default='Anonymous', help_text='Please enter preferred name/nickname for personalized communication', max_length=150),
        ),
    ]