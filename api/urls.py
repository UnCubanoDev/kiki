from rest_framework import routers
from .views import (
    RestaurantViewSet,
    CategoryViewSet,
    OrderViewSet,
    DistributorViewSet,
    ProductViewSet,
    ProductCategoryViewSet
)

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'distributors', DistributorViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-category', ProductCategoryViewSet)

urlpatterns = router.urls
