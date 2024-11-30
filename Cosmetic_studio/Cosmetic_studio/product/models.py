from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class Product(models.Model):
    MAX_NAME_LENGTH = 30
    MAX_DESCRIPTION_LENGTH = 600
    MAX_BRAND_LENGTH = 20

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )

    brand = models.CharField(
        max_length=MAX_BRAND_LENGTH,
    )

    description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH,
    )

    image = models.ImageField(
        upload_to='products/',
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    units_sold = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    slug = models.SlugField(
        unique=True,
        editable=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        num = 1
        if not self.slug:
            self.slug = slugify(f'{self.brand}-{self.name}-{num}')

        original_slug = self.slug
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{num}"
            num += 1
        super().save(*args, **kwargs)
