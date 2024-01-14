from rest_framework import status
from rest_framework.response import Response
from directorio.serializers import ChangePasswordSerializer, PhoneSerializer, UserSignupSerializer

# Django REST Framework
from rest_framework import status, viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import exceptions

# Serializers
from directorio.serializers import UserLoginSerializer, UserModelSerializer, UpdateUserSerializer, AddressSerializer
from api.serializers import DistributorSerializer, RestaurantSerializer

# Models
from directorio.models import User, Address
from api.models import Distributor, Restaurant

#RestorePassword
from directorio.helper import _unicode_ci_compare, send_whatsapp_message
from django_rest_passwordreset.views import ResetPasswordRequestTokenViewSet
from django_rest_passwordreset.models import get_password_reset_token_expiry_time, clear_expired, ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

#AccountConfirmation
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')

class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserModelSerializer
        return UpdateUserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class UserInfoView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserModelSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SignupView(generics.GenericAPIView):

    serializer_class = UserSignupSerializer

    def sendActivationLink(self, user):
        site = get_current_site(self.request)
        activation_url = f"http://{site.domain}/api/auth/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}"
        message = f'\nPara activar tu cuenta, por favor haz clic en el siguiente enlace:\n{activation_url}'
        send_whatsapp_message(message, user.phone[1:])

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.sendActivationLink(user)
        user_response = UserModelSerializer(instance=user).data
        return Response(user_response, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'access_token': token,
            'user': UserModelSerializer(instance=user).data,
        }
        distributors = Distributor.objects.filter(user=user)
        restaurants = Restaurant.objects.filter(user=user)
        if len(distributors) > 0:
            data['distributor'] = DistributorSerializer(
                instance=distributors[0]).data
        if len(restaurants) > 0:
            data['restaurant'] = RestaurantSerializer(
                instance=restaurants[0]).data
        return Response(data, status=status.HTTP_201_CREATED)

class ChangePasswordView(generics.GenericAPIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, instance=request.user, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class ResetPasswordRequestToken(generics.GenericAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = PhoneSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)
  
        clear_expired(now_minus_expiry_time)

        users = User.objects.filter(phone=phone)

        active_user_found = False

        for user in users:
            if user.eligible_for_reset():
                active_user_found = True
                break

        if not active_user_found and not getattr(settings, 'DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE', False):
            raise exceptions.ValidationError({
                'phone': [(
                    "We couldn't find an account associated with that phone. Please try a different phone")],
            })

        for user in users:
            if user.eligible_for_reset() and \
                    _unicode_ci_compare(phone, getattr(user, 'phone')):
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    print("KKK -------------- LLL")
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
                        ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(sender=self.__class__, instance=self, reset_password_token=token)
        # done
        return Response({'status': 'OK'})

class PhoneResetPasswordRequestToken(ResetPasswordRequestToken, viewsets.GenericViewSet):
    serializer_class = PhoneSerializer

    def create(self, request, *args, **kwargs):
        return super(PhoneResetPasswordRequestToken, self).post(request, *args, **kwargs)
    
@api_view(['GET',])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response('La activación fue exitosa.', status=status.HTTP_200_OK)
    else:
        return Response('El enlace de activación es inválido.', status=status.HTTP_400_BAD_REQUEST)