import datetime

from django.utils.http import urlencode
from reportlab.pdfgen import canvas
from reportlab_qrcode import QRCodeImage

from ..models import OrderItem, BoughtTour
from .generate_token import generate_token_for_qr_code


def write_pdf(order_item: OrderItem, bought_tour:BoughtTour):
    file_name = f"pdfs/{order_item.id}_tickets.pdf"
    logo = 'images/logo.jpg'

    pdf = canvas.Canvas(file_name)

    token = generate_token_for_qr_code(bought_tour)

    qr_data = "http://127.0.0.1:8080/tours/ticket-check/"  + "?" + urlencode({"token": token})
    qr_code = QRCodeImage(qr_data, size=200)
    qr_code.drawOn(pdf, 380, 630)

    pdf.line(390, 640, 570, 640)
    pdf.line(390, 820, 570, 820)
    pdf.line(390, 640, 390, 820)
    pdf.line(570, 640, 570, 820)

    pdf.setTitle("Your tickets")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawImage(logo, 40, 760, 60, 60)
    pdf.drawString(170, 780, f"Tickets for {order_item.tour}:")

    pdf.line(20, 700, 280, 700)

    y = 700
    ticket_number = bought_tour.amount
    seat_number = bought_tour.tour.tickets_amount
    seat_number += order_item.amount
    seat_numbers = []
    start = 1
    stop = order_item.amount
    stop += 1


    pdf.setFont("Helvetica-Bold", 15)

    pdf.drawString(65, 710, f"Tickets:")
    pdf.drawString(190, 710, f"Seats:")
    pdf.drawString(320, 600, f"Details:")

    pdf.setFont("Helvetica", 12)

    for _ in range(start, stop):
        ticket_number += 1
        y -= 30
        pdf.drawString(65, y, f"Ticket #{ticket_number}")
        pdf.drawString(190, y, f"Seat #{seat_number}")
        seat_numbers.append(seat_number)
        seat_number-= 1

    final_seat_numbers = bought_tour.seats
    final_seat_numbers.extend(seat_numbers)

    bought_tour.seats = final_seat_numbers
    bought_tour.save()

    y -= 30

    pdf.line(150, 700, 150, y)
    pdf.line(280, 700, 280, y)
    pdf.line(20, 700, 20, y)
    pdf.line(20, y, 280, y)

    y -= 30

    pdf.line(20, y, 280, y)

    y -= 15

    pdf.drawString(20, y, 'Your Zentour team')

    pdf.line(320, 590, 570, 590)

    now = datetime.datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")

    pdf.drawString(330, 570, f"Purchased on {formatted}")
    pdf.drawString(330, 540, f"Total price: ${order_item.item_total}")
    pdf.drawString(
        330, 510, f"Tour Dates: {order_item.tour.start_date} - {order_item.tour.end_date}"
    )
    pdf.drawString(330, 480, f"Tickets amount: {order_item.amount}")
    pdf.drawString(330, 450, f"Contact email: {order_item.order.contact_email}")
    pdf.drawString(330, 420, f"Contact phone: {order_item.order.contact_phone}")
    pdf.drawString(330, 390, f"Cities: {order_item.tour.cities}")

    pdf.line(320, 590, 320, 360)
    pdf.line(570, 590, 570, 360)
    pdf.line(320, 360, 570, 360)

    pdf.save()

    return file_name
