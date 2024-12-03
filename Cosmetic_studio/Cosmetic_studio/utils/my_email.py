import time

from asgiref.sync import sync_to_async
from django.core.mail import send_mail
import asyncio


async def send_simple_email(subject, message, recipient_list):
    await sync_to_async(send_mail)(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=None,
        fail_silently=False,
    )
    await asyncio.sleep(5)


def send_simple_email_sync(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=None,
        fail_silently=False,
    )
    time.sleep(5)
