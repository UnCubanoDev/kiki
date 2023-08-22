# Generated by Django 4.1.1 on 2023-08-22 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directorio', '0003_address'),
        ('api', '0031_remove_order_delivery_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='directorio.address', verbose_name='delivery address'),
            preserve_default=False,
        ),
    ]
