from django.contrib import admin

from .models import (Restaurant, Category, Distributor, DistributorRating,
                     OrderDetail, ProductRating, Product, Order, RestaurantRating)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone',
                    'user', 'tax', 'is_active', 'rating']
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_id', 'vehicle_type', 'rating']
    pass


@admin.register(DistributorRating)
class DistributorRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'restaurant',
        'price',
        'um',
        'category',
        'rating',
    ]
    pass


@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date',
        'time',
        'status',
    ]
    pass
