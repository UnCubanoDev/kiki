from rest_framework import serializers
from .models import (Restaurant, RestaurantRating, Category,
                     Distributor, Order, Product, ProductRating, OrderDetail, DistributorRating)
from directorio.models import User
from directorio.serializers import UserModelSerializer


class DistributorRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = DistributorRating
        fields = '__all__'


class RestaurantRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = RestaurantRating
        fields = '__all__'


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = ProductRating
        fields = '__all__'


class DistributorSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = Distributor
        fields = [
            'id',
            'user',
            'vehicle_image',
            'vehicle_id',
            'vehicle_type',
            'user',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all())

    restaurant = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'time',
            'image',
            'category',
            'restaurant',
            'amount',
        ]


class RestaurantSerializer(serializers.ModelSerializer):

    user = UserModelSerializer()
    products = ProductSerializer(many=True)
    categories_product = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all(), many=True)

    def save(self, **kwargs):
        return super().save(**kwargs)

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
            'rating',
            'products',
            'categories_product',
            'type',
            'latitude',
            'longitude',
        ]


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ['product', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    products = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'products',
            'date',
            'time',
            'delivery_address',
            'pay_type',
            'total_price',
            'bussinness_addresses',
        ]
        read_only_fields = [
            'id',
            'date',
            'time',
            'status'
            'total_price',
        ]

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for order_detail in products_data:
            OrderDetail.objects.create(
                order=order, product=order_detail['product'], amount=order_detail['amount'])
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            'id',
            'order',
            'product',
            'amount',
        ]
