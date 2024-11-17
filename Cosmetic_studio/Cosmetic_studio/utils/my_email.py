from django.core.mail import send_mail

from Cosmetic_studio import settings


def send_simple_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=settings.DEFAULT_FROM_EMAIL,
    )

