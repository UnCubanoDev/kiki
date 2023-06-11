from multiprocessing import context
from urllib import request
from rest_framework import status
from rest_framework.response import Response
from directorio.serializers import ChangePasswordSerializer, UpdateUserSerializer, UserSignupSerializer

# Django REST Framework
from rest_framework import status, viewsets, generics, mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Serializers
from directorio.serializers import UserLoginSerializer, UserModelSerializer

# Models
from directorio.models import User

class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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
    
class SignupView(generics.GenericAPIView):

    serializer_class = UserSignupSerializer

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
class LoginView(generics.GenericAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(instance=user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
class ChangePasswordView(generics.GenericAPIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, instance=request.user, context= {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)