# Generated by Django 5.1.2 on 2024-11-26 17:05

import Cosmetic_studio.utils.blog_mixins
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
            bases=(Cosmetic_studio.utils.blog_mixins.FieldSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlogContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(3)])),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('main_image', models.ImageField(upload_to='blog_images/')),
                ('left_image', models.ImageField(upload_to='blog_images/')),
                ('right_image', models.ImageField(upload_to='blog_images/')),
                ('content', models.TextField(max_length=3000, validators=[django.core.validators.MinLengthValidator(20)])),
                ('blockquote', models.TextField(blank=True, help_text='A highlighted quote or excerpt from the content.', max_length=320, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='blogs', to='blog.tag')),
            ],
            bases=(Cosmetic_studio.utils.blog_mixins.FieldSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.blogcontent', verbose_name='Post')),
            ],
        ),
    ]
