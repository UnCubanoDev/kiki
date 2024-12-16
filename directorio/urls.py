from django.urls import path, include
from .views import PhoneResetPasswordRequestToken, UserViewSet, ChangePasswordView, SignupView, LoginView, AddressViewSet, UserInfoView, activate, privacy_policy
from rest_framework import routers
from django_rest_passwordreset.views import ResetPasswordConfirmViewSet, ResetPasswordValidateTokenViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'password_reset', PhoneResetPasswordRequestToken, basename='reset-password-request')
router.register(r'password_reset/validate_token', ResetPasswordValidateTokenViewSet, basename='reset-password-validate')
router.register(r'password_reset/confirm', ResetPasswordConfirmViewSet, basename='reset-password-confirm')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('users/me/', UserInfoView.as_view(), name='auth_info'),
    path('signup/', SignupView.as_view(), name='auth_signup'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_chpass'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('privacidad/', privacy_policy, name='privacy_policy'),
]