import os

from django.core.mail import EmailMessage

from ..models import OrderItem, BoughtTour
from .create_pdf import write_pdf


def send_email_with_attachment(
    subject, message, from_email, recipient_list, order_item: OrderItem, bought_tour:BoughtTour
):
    file_name = write_pdf(order_item, bought_tour)

    with open(file_name, "rb") as file:
        file_content = file.read()
        full_file_name = os.path.basename(file_name)

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(full_file_name, file_content)
    email.send()
