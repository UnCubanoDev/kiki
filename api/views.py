from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsDistributor, IsReadOnly, IsProductOwner

from .models import Restaurant, Order, Category, Distributor, Product
from .serializers import (RestaurantSerializer, CategorySerializer,
                          OrderSerializer, DistributorSerializer, ProductSerializer, OrderDetailSerializer,)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsDistributor | IsReadOnly | IsProductOwner]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsDistributor | IsReadOnly | IsProductOwner]


class DistributorViewSet(viewsets.ModelViewSet):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer
    # permission_classes = [IsDistributor | IsReadOnly | IsProductOwner]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsDistributor | IsReadOnly | IsProductOwner]
