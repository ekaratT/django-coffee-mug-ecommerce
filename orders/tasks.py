from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from base import settings


@shared_task
def order_created(order_id):
    """
    Task for sending email when the order is successfully created.
    """

    order = Order.objects.get(id=order_id)
    subject = f'COFFEE-MUG order number: {order_id}'
    message = f'Dear {order.first_name},\n\n' \
        f'Your order have been placed successfully.'\
        f'Your order id is {order_id}.'
    mail_sent = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[order.email])

    return mail_sent



    