from django.db import models


class TeamMemberCard(models.Model):
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        upload_to='team_pictures/',
        verbose_name='Profile Picture',
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=300,
        verbose_name='Card Title',
        blank=True,
        null=True,
    )

    description = models.TextField(
        verbose_name='Card Description',
        blank=True,
        null=True,
    )

    role = models.CharField(
        max_length=100,
        verbose_name='Role',
        blank=True,
        null=True,
    )

    specialities = models.TextField(
        verbose_name='Specialties',
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At',
    )

    appearance_order = models.PositiveIntegerField(
        default=2,
        verbose_name='Ordering',
    )

    class Meta:
        verbose_name = "Team Member Card"
        verbose_name_plural = "Team Member Cards"
        ordering = ['appearance_order', '-updated_at']

    def __str__(self):
        return self.name


class IndexPageAds(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Advertisement Name',
        blank=True,
        null=True,
    )

    adv_description = models.TextField(
        verbose_name='Advertisement Description',
        blank=True,
        null=True,
    )

    adv_link = models.URLField(
        verbose_name='Advertisement Link',
        blank=True,
        null=True,
    )

    adv_image = models.ImageField(
        upload_to='ads/',
        verbose_name='Advertisement Image',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
    )


