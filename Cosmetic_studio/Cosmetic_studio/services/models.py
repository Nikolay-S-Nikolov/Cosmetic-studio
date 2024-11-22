from django.db import models
from Cosmetic_studio.utils.services_mixins import TimestampedUserMixin


# Create your models here.
class Services(TimestampedUserMixin):
    name = models.CharField(
        max_length=150,
    )

    subheading = models.CharField(
        max_length=150,
    )

    main_image = models.ImageField(
        upload_to='services/',
        verbose_name='Main Image',
    )

    description = models.TextField(
        verbose_name='Description',
    )

    def __str__(self):
        return self.name


class ServicePricing(TimestampedUserMixin):
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        verbose_name='Pricing',
    )

    service_type = models.CharField(
        max_length=100,
        verbose_name='Service Type',
    )

    treatment_description = models.TextField(
    )

    price = models.PositiveIntegerField(
        verbose_name='Price',
    )

    def __str__(self):
        return f'{self.service} - {self.service_type} price {self.price}'


class ServicePictures(TimestampedUserMixin):
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        verbose_name='Pictures',
    )

    image = models.ImageField(
        upload_to='services/',
        verbose_name='Image',
    )

    def __str__(self):
        return f'Image {self.id} for {self.service}'
