from django.contrib import admin

from .models import (Restaurant, Category, Distributor,
                     OrderDetail, ProductRating, Product, Order, RestaurantRating)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
