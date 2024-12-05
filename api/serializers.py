from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (Restaurant, RestaurantRating, Category, Configuration, 
                     Distributor, Order, Product, ProductRating, OrderDetail, DistributorRating, ProductCategory, Metrics)
from directorio.serializers import UserModelSerializer, AddressSerializer
from directorio.models import Address
from .helpers import calculate_price
from django.utils import timezone
from datetime import time
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SuperClientsSerializer(serializers.Serializer):
    user = UserModelSerializer()
    total = serializers.IntegerField()


class MetricsSerializer(serializers.ModelSerializer):
    super_clients = SuperClientsSerializer(many=True)

    class Meta:
        model = Metrics
        fields = [
            'super_clients'
        ]


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
            'rating',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all())

    restaurant_id = serializers.PrimaryKeyRelatedField(read_only=True, source='restaurant')
    price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

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
            'restaurant_id',
            'amount',
            'rating',
            'currency',
        ]

    def get_price(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return obj.price
            
        return calculate_price(
            base_price=obj.price,
            restaurant_tax=obj.restaurant.tax,
            user=request.user
        )

    def get_currency(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 'USD'
            
        return 'CUP' if request.user.phone.startswith('+53') else 'USD'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = [
            'business'
        ]


class RestaurantSerializer(serializers.ModelSerializer):

    user = UserModelSerializer()
    products = ProductSerializer(many=True)
    bussiness_type = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all(), many=True)
    categories_product = serializers.SlugRelatedField(
        slug_field='name', queryset=ProductCategory.objects.all(), many=True)

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
            'bussiness_type',
            'categories_product',
            'latitude',
            'longitude',
            'recommended',
            'funds'
        ]


class OrderProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all())

    restaurant = RestaurantSerializer(read_only=True)

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


class OrderProductsSerializer(serializers.Serializer):
    detail = OrderProductDetailSerializer(read_only=True)
    amount = serializers.IntegerField()


class BusinessOrderSerializer(serializers.Serializer):
    latitude = serializers.CharField(read_only=True)
    longitude = serializers.CharField(read_only=True)
    products = OrderProductsSerializer(many=True)


class OrderDetailSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderDetail
        fields = ['id', 'product', 'quantity', 'unit_price', 'final_price']
        
    def get_final_price(self, obj):
        return obj.get_final_price()


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    business_orders = BusinessOrderSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)
    products = OrderDetailSerializer(many=True, write_only=True)
    distributor = DistributorSerializer(read_only=True)
    delivery_address = AddressSerializer(read_only=True)
    delivery_address_id = serializers.IntegerField(write_only=True)
    details = OrderDetailSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'distributor',
            'products',
            'date',
            'time',
            'delivery_address',
            'delivery_address_id',
            'pay_type',
            'sub_total',
            'delivery_price',
            'total_price',
            'business_orders',
            'status',
            'delivery_total_distance',
            'details',
            'total',
        ]
        read_only_fields = [
            'id',
            'date',
            'time',
            'total_price',
            'distributor',
        ]

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        delivery_address = validated_data.pop('delivery_address_id')
        delivery_address = Address.objects.get(pk=delivery_address)
        order = Order.objects.create(delivery_address= delivery_address, **validated_data)
        for order_detail in products_data:
            OrderDetail.objects.create(
                order=order, product=order_detail['product'], amount=order_detail['amount'])
        return order

    def get_total(self, obj):
        return sum(detail.get_final_price() for detail in obj.orderdetail_set.all())

    def validate(self, attrs):
        current_time = timezone.localtime().time()
        config = Configuration.objects.first()
        
        if not config:
            return attrs
            
        if current_time >= config.business_closing_time or \
           current_time < config.business_opening_time:
            raise serializers.ValidationError(
                _('Lo sentimos, los negocios están cerrados. '
                  'Horario de atención: {opening} - {closing}').format(
                    opening=config.business_opening_time.strftime('%H:%M'),
                    closing=config.business_closing_time.strftime('%H:%M')
                )
            )
            
        return super().validate(attrs)


class RestaurantMetricsOrdersSerializer(serializers.Serializer):
    pending = serializers.IntegerField()
    canceled = serializers.IntegerField()
    delivered = serializers.IntegerField()


class RestaurantMetricsSerializer(serializers.Serializer):
    total_month = serializers.ListField(child=serializers.FloatField())
    total_month_gain = serializers.FloatField()
    total_month_tax = serializers.FloatField()
    total_month_gain_clean = serializers.FloatField()
    orders = RestaurantMetricsOrdersSerializer()


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'