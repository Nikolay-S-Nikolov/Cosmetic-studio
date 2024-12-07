from django.db import models

from Cosmetic_studio.utils.services_mixins import TimestampedUserMixin


# Create your models here.
class Services(TimestampedUserMixin):
    MAX_NAME_LENGTH = 150
    MAX_SUBHEADING_LENGTH = 150
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )

    subheading = models.CharField(
        max_length=MAX_SUBHEADING_LENGTH,
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
    MAX_SERVICE_TYPE_LENGTH = 100
    """
    You can include BENEFITS as ServicePricing model without price
    """
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        verbose_name='Service',
        related_name='pricing',
    )

    service_type = models.CharField(
        max_length=MAX_SERVICE_TYPE_LENGTH,
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
        verbose_name='Service',
        related_name='pictures',
    )

    image = models.ImageField(
        upload_to='services/',
        verbose_name='Image',
    )

    def __str__(self):
        return f'Image {self.id} for {self.service}'

