# Generated by Django 4.1.1 on 2023-06-11 22:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_productrate_productrating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productrating',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='restaurantrating',
            name='rate',
        ),
        migrations.AddField(
            model_name='productrating',
            name='rating',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'at least 1'), django.core.validators.MaxValueValidator(5, 'max 5')], verbose_name='rating'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurantrating',
            name='rating',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'at least 1'), django.core.validators.MaxValueValidator(5, 'max 5')], verbose_name='rating'),
            preserve_default=False,
        ),
    ]
