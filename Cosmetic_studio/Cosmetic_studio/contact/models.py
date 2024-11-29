from django.core.validators import RegexValidator
from django.db import models


class ContactInfo(models.Model):
    MAX_PHONE_NUMBER_LENGTH = 10
    phone_number = models.CharField(
        max_length=MAX_PHONE_NUMBER_LENGTH,
        validators=[RegexValidator(
            regex=r"^0\d{9}$",
            message="Please, enter a valid phone number in the format 0888123456"
        )],
    )
    working_time = models.TextField()
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    custom_message = models.TextField()
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact Information: {self.phone_number}"
