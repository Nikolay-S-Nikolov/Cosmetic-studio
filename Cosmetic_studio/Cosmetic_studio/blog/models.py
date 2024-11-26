from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from Cosmetic_studio.utils.blog_mixins import FieldSlugMixin

UserModel = get_user_model()


class BlogContent(FieldSlugMixin, models.Model):
    MAX_TITLE_LENGTH = 60
    MIN_TITLE_LENGTH = 3
    MAX_CONTENT_LENGTH = 3000
    MIN_CONTENT_LENGTH = 20

    slug_field = "title"

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        validators=[MinLengthValidator(MIN_TITLE_LENGTH)],
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    content = models.TextField()

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    published = models.BooleanField(default=False)

    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


# class Category(FieldSlugMixin, models.Model):
#     MAX_NAME_LENGTH = 100
#
#     name = models.CharField(max_length=MAX_NAME_LENGTH)
#
#     slug = models.SlugField(unique=True)
#
#     description = models.TextField(blank=True)
#
#     posts = models.ManyToManyField(
#         BlogContent,
#         related_name='categories'
#     )
#
#     def __str__(self):
#         return self.name


class Comment(models.Model):
    post = models.ForeignKey(
        BlogContent,
        verbose_name='Post',
        related_name='comments',
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        UserModel,
        related_name='comments',
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


class Tag(FieldSlugMixin, models.Model):
    MAX_NAME_LENGTH = 50

    name = models.CharField(max_length=MAX_NAME_LENGTH)

    slug = models.SlugField(unique=True)

    posts = models.ManyToManyField(
        BlogContent,
        related_name='tags',
    )

    def __str__(self):
        return self.name


class Image(models.Model):
    MAX_CAPTION_LENGTH = 255

    post = models.ForeignKey(
        BlogContent,
        verbose_name='Post',
        on_delete=models.CASCADE,
        related_name='images',
    )

    image = models.ImageField(
        upload_to='blog_images/',
    )

    caption = models.CharField(
        max_length=MAX_CAPTION_LENGTH,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Image for {self.post.title}'
