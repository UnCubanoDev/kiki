from datetime import date
from calendar import monthrange
import math
from django.db.models import Count
from rest_framework import viewsets, status, generics, views
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsDistributor, IsReadOnly, IsProductOwner, IsProvider, IsClientAndOrderOwner, IsOrderPending

from .models import Restaurant, Order, Category, Distributor, Product, ProductCategory, Metrics, OrderDetail, Configuration
from .serializers import (RestaurantSerializer, CategorySerializer,
                          OrderSerializer, DistributorSerializer, ProductSerializer,
                          ProductRatingSerializer, RestaurantRatingSerializer,
                          DistributorRatingSerializer, ProductCategorySerializer, MetricsSerializer,
                          RestaurantMetricsSerializer, ConfigurationSerializer
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

    @method_decorator(cache_page(30))
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

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[],
        serializer_class=RestaurantMetricsSerializer
    )
    def metrics(self, request, pk=None):
        business = Restaurant.objects.get(pk=pk)
        month = request.query_params.get('month') or date.today().month
        year = request.query_params.get('year') or date.today().year
        orders = OrderDetail.objects.filter(
            order__date__year=year,
            order__date__month=month,
            product__restaurant=business
        )
        total_month = []
        total_month_gain = 0
        month_days = monthrange(int(year), int(month))[1]
        delivered_orders = orders.filter(order__status='delivered')
        for month_day in range(1, month_days + 1):
            day_gain = sum([order.price for order in delivered_orders.filter(
                order__date__day=int(month_day))])
            total_month.append(day_gain)
            total_month_gain += day_gain
        orders_by_status = orders.values('order__status').annotate(
            count=Count('order__status')).order_by()
        orders_status = {
            'delivered': 0,
            'pending': 0,
            'canceled': 0,
        }
        for os in orders_by_status:
            if os['order__status'] in ['pending', 'assigned', 'on the way']:
                orders_status['pending'] += os['count']
            else:
                orders_status[os['order__status']] = os['count']
        serializer = RestaurantMetricsSerializer(
            {
                'total_month': total_month,
                'total_month_gain': math.ceil(total_month_gain),
                'total_month_tax': math.ceil(float(total_month_gain) * float(business.tax) / 100),
                'total_month_gain_clean': math.floor(float(total_month_gain) - float(float(total_month_gain) * float(business.tax) / 100)),
                'orders': orders_status
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        permission_classes=[IsClientAndOrderOwner, IsOrderPending],
        serializer_class=None
    )
    def cancel(self, request, pk):
        """
            Action when the client cancels the order and turns the `status` to "`canceled`"
        """
        order = Order.objects.get(pk=pk)
        distributor = Distributor.objects.get(user=request.user)
        if order.distributor != distributor:
            Response(status=status.HTTP_403_FORBIDDEN)
        if order.status == 'assigned':
            order.status = 'canceled'
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

    @method_decorator(cache_page(30))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(restaurant=Restaurant.objects.get(
            user=self.request.user))

    def perform_update(self, serializer):
        instance = serializer.instance
        original_product = Product.objects.get(pk=instance.pk)
        old_price = original_product.price
        old_pk = original_product.pk
        serializer.save()
        print(instance.price)
        print(original_product.price)
        if instance.price != original_product.price:
            instance.pk = None
            new = instance.save()
            print(new)
            old_product = Product.objects.get(pk=old_pk)
            print(old_product)
            old_product.is_active = False
            old_product.price = old_price
            old_product.save()
        else:
            serializer.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        serializer_class=ProductRatingSerializer
    )
    def rate(self, request):
        return super_rate(request, 'product', self.get_serializer, Product)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsProvider | IsReadOnly]

    def get_queryset(self):
        return ProductCategory.objects.filter(business=Restaurant.objects.get(user=self.request.user))

    def perform_create(self, serializer):
        return serializer.save(business=Restaurant.objects.get(user=self.request.user))


class MetricsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MetricsSerializer

    def get_object(self):
        return Metrics.get_solo()


class ConfigurationApiView(views.APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        config = Configuration.objects.get(pk=1)
        serializer = ConfigurationSerializer(config)
        return Response(serializer.data)

    def put(self, request):
        config = Configuration.objects.get(pk=1)
        serializer = ConfigurationSerializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


