from django.urls import path, include
from .views import UserViewSet, ChangePasswordView, SignupView, LoginView
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('signup/', SignupView.as_view(), name='auth_signup'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_chpass'),
    path('password_reset/', include('django_rest_passwordreset.urls',
         namespace='password_reset')),
]
