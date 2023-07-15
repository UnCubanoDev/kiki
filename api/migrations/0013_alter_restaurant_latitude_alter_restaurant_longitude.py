# Generated by Django 4.1.1 on 2023-07-15 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_restaurant_latitude_restaurant_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='latitude',
            field=models.CharField(default='', max_length=25, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='longitude',
            field=models.CharField(default='', max_length=25, verbose_name='longitude'),
        ),
    ]
