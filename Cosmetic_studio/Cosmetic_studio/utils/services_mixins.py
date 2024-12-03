from django.contrib.auth import get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.db import models

UserModel = get_user_model()


class TimestampedUserMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At',
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='User',
    )

    class Meta:
        abstract = True


class OnlyForStaffMixin(auth_mixins.UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
