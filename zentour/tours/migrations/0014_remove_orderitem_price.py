# Generated by Django 5.2.4 on 2025-07-25 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0013_boughttour_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
    ]
