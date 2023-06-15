from django.urls import path, include
from rest_framework import routers
from .views import RestaurantViewSet

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = router.urls
