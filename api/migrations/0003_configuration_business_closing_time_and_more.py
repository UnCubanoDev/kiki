# Generated by Django 4.1.1 on 2024-12-05 10:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_orderdetail_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='business_closing_time',
            field=models.TimeField(default=datetime.time(23, 59), verbose_name='business closing time'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='business_opening_time',
            field=models.TimeField(default=datetime.time(8, 0), verbose_name='business opening time'),
        ),
    ]
