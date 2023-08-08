from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import (Restaurant, Category, Distributor, DistributorRating,
                     OrderDetail, ProductRating, Product, Order, RestaurantRating, Configuration)

from solo.admin import SingletonModelAdmin


@admin.register(Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'address',
        'phone',
        'user',
        'tax',
        'is_active',
        'rating',
        'total_gain',
        'total_gain_clean',
        'debt',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_id',
                    'vehicle_type', 'rating', 'total_gain']
    pass


@admin.register(DistributorRating)
class DistributorRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'business',
        'amount',
        'was_paid_by_business',
    ]
    search_fields = [
        'order',
        'business',
        'product',
    ]
    list_filter = [
        'was_paid_by_business',
    ]


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'id',
        'restaurant',
        'price',
        'um',
        'category',
        'rating',
        'is_active',
    ]
    list_filter = ['is_active']


@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date',
        'time',
        'delivery_address',
        'status',
        'pay_type',
    ]
