from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsDistributor, IsReadOnly, IsProductOwner, IsProvider, IsOrderDistributor

from .models import Restaurant, Order, Category, Distributor, Product, ProductRating, RestaurantRating, DistributorRating
from .serializers import (RestaurantSerializer, CategorySerializer,
                          OrderSerializer, DistributorSerializer, ProductSerializer,
                          OrderDetailSerializer, ProductRatingSerializer, RestaurantRatingSerializer,
                          DistributorRatingSerializer
                          )

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


def super_rate(request, instance, serializer, model):
    user = request.user
    instance_data = request.data[instance]
    rating = request.data['rating']
    data = {
        'user': user,
        instance: instance_data,
        'rating': rating,
    }
    serializer_instance = serializer(data=data)
    if serializer_instance.is_valid():
        try:
            model.objects.get(pk=request.data[instance]).rate(
                user=user, rating=rating)
            return Response(serializer_instance.data,
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer_instance.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    # permission_classes = [IsAdminUser]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
        serializer_class=RestaurantRatingSerializer
    )
    def rate(self, request):
        return super_rate(request, 'restaurant', self.get_serializer, Restaurant)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsDistributor | IsReadOnly | IsProductOwner]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated | IsReadOnly]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsDistributor],
        serializer_class=None
    )
    def accept(self, request, pk):
        """
            Action when the distributor accepts the order and turns the `status` to "`on the way`"
        """
        order = Order.objects.get(pk=pk)
        distributor = Distributor.objects.get(user=request.user)
        if order.distributor != distributor:
            Response(status=status.HTTP_403_FORBIDDEN)
        if order.status == 'assigned':
            order.status = 'on the way'
            order.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsDistributor],
        serializer_class=None
    )
    def deliver(self, request, pk):
        """
            Action when the distributor finshes the shipment and turns the `status` to "`delivered`"
        """
        order = Order.objects.get(pk=pk)
        distributor = Distributor.objects.get(user=request.user)
        if order.distributor != distributor:
            Response(status=status.HTTP_403_FORBIDDEN)
        if order.status == 'on the way':
            order.status = 'delivered'
            order.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsDistributor],
        serializer_class=OrderSerializer
    )
    def assigned(self, request):
        distributor = Distributor.objects.get(user=request.user)
        serializer = self.get_serializer(
            data=Order.objects.filter(distributor=distributor, status='assigned'), many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsDistributor],
        serializer_class=OrderSerializer
    )
    def accepted(self, request):
        distributor = Distributor.objects.get(user=request.user)
        serializer = self.get_serializer(
            data=Order.objects.filter(distributor=distributor, status='on the way'), many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsDistributor],
        serializer_class=OrderSerializer
    )
    def delivered(self, request):
        distributor = Distributor.objects.get(user=request.user)
        serializer = self.get_serializer(
            data=Order.objects.filter(distributor=distributor, status='delivered'), many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')


class DistributorViewSet(viewsets.ModelViewSet):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer
    # permission_classes = [IsDistributor | IsReadOnly | IsProductOwner]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        serializer_class=DistributorRatingSerializer
    )
    def rate(self, request):
        return super_rate(request, 'distributor', self.get_serializer, Distributor)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsProvider | IsReadOnly | IsProductOwner]

    @method_decorator(cache_page(120))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(restaurant=Restaurant.objects.get(
            user=self.request.user))

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        serializer_class=ProductRatingSerializer
    )
    def rate(self, request):
        return super_rate(request, 'product', self.get_serializer, Product)
