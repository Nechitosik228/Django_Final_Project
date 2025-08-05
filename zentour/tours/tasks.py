import datetime

from celery import shared_task

from .models import CartItem

@shared_task
def delete_old_cart_items():
    time = datetime.datetime.now() - datetime.timedelta(minutes=5)
    items = CartItem.objects.filter(timestamp__lt=time)
    for item in items:
        item.tour.tickets_amount += item.amount
        item.tour.save()
    items.delete()
    
