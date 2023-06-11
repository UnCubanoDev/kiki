from rest_framework import serializers
from .models import (Restaurant, RestaurantRating, Category,
                     Distributor, Order, Product, ProductRating, OrderDetail)
from directorio.models import User
from directorio.serializers import UserModelSerializer


class RestaurantSerializer(serializers.ModelSerializer):

    user = UserModelSerializer()

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'description',
            'address',
            'phone',
            'image',
            'user',
            'time',
            'rating'
        ]


class RestaurantRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRating
        fields = '__all__'


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = [
            'id',
            'user',
            'vehicle_image',
            'vehicle_id',
            'vehicle_type',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'products',
            'date',
            'time',
            'address',
            'status',
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            'id',
            'order',
            'product',
            'amount',
        ]
