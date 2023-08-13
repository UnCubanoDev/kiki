from rest_framework import serializers
from .models import (Restaurant, RestaurantRating, Category,
                     Distributor, Order, Product, ProductRating, OrderDetail, DistributorRating, ProductCategory)
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
            'type',
            'latitude',
            'longitude',
            'recommended',
        ]


class OrderProductsSerializer(serializers.Serializer):
    detail = ProductSerializer(read_only=True)
    amount = serializers.IntegerField()


class BusinessOrderSerializer(serializers.Serializer):
    latitude = serializers.CharField(read_only=True)
    longitude = serializers.CharField(read_only=True)
    products = OrderProductsSerializer(many=True)


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ['product', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    business_orders = BusinessOrderSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)
    products = OrderDetailSerializer(many=True, write_only=True)
    distributor = DistributorSerializer(read_only=True)

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
            'pay_type',
            'sub_total',
            'delivery_price',
            'total_price',
            'business_orders',
            'status',
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
