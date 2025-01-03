# Generated by Django 4.1.1 on 2024-12-11 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_product_thermopack_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='api.restaurant'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
