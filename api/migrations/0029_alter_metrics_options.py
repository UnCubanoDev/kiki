# Generated by Django 4.1.1 on 2023-08-22 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_metrics_alter_restaurant_bussiness_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metrics',
            options={'verbose_name': 'Metrics'},
        ),
    ]