import datetime

from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab_qrcode import QRCodeImage

from ..models import OrderItem


def write_pdf(order_item:OrderItem):
    file_name = f"pdfs/{order_item.order.id}_tickets.pdf"

    pdf = canvas.Canvas(file_name)

    qr_data = 'localhost:8080/tours/bought_tours/'
    qr_code = QRCodeImage(qr_data, size=200)
    qr_code.drawOn(pdf, 380, 630)

    pdf.setTitle("Your tickets")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(40, 780, f"Tickets for {order_item.tour}:")

    pdf.line(20, 700, 280, 700)

    pdf.setFont("Helvetica", 12)

    y = 700
    ticket_number = 0
    start = 1
    stop = 0
    stop += 1
    stop += order_item.amount

    pdf.drawString(65, 710, f"Tickets:")
    pdf.drawString(190, 710, f"Seats:")

    for i in range(start, stop):
        ticket_number += 1
        y -= 30
        pdf.drawString(65, y, f"Ticket #{i}")
        pdf.drawString(190, y, f"Seat #{i}")

    y -= 30
    
    pdf.line(150, 700, 150, y)
    pdf.line(280, 700, 280, y)
    pdf.line(20, 700, 20, y)
    pdf.line(20, y, 280, y)

    pdf.drawString(320, 600, f"Details:")

    pdf.line(320, 590, 570, 590)


    now = datetime.datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")

    pdf.drawString(330, 570, f"Purchased on {formatted}")
    pdf.drawString(330, 540, f"Total price: ${order_item.item_total}")
    pdf.drawString(330, 510, f"Dates: {order_item.tour.start_date} - {order_item.tour.end_date}")
    pdf.drawString(330, 480, f"Tickets amount: {order_item.amount}")
    pdf.drawString(330, 450, f"Contact email: {order_item.order.contact_email}")
    pdf.drawString(330, 420, f"Contact phone: {order_item.order.contact_phone}")
    pdf.drawString(330, 390, f"Cities: {order_item.tour.cities}")

    pdf.line(320, 590, 320, 360)
    pdf.line(570, 590, 570, 360)
    pdf.line(320, 360, 570, 360)

    pdf.save()

    return file_name
