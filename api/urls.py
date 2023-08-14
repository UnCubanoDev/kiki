from django.urls import path
from rest_framework import routers
from .models import Metrics
from .views import (
    RestaurantViewSet,
    CategoryViewSet,
    OrderViewSet,
    DistributorViewSet,
    ProductViewSet,
    ProductCategoryViewSet,
    MetricsRetrieveAPIView
)

router = routers.DefaultRouter()

router.register(r'restaurants', RestaurantViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'distributors', DistributorViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-category', ProductCategoryViewSet)

urlpatterns = [
    path('metrics/', MetricsRetrieveAPIView.as_view(queryset=Metrics.get_solo()))
]

urlpatterns += router.urls
