from directorio.models import User, Address
from django.contrib.auth import authenticate, password_validation

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = [
            'user',
        ]


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        exclude = (
            'password',
            'last_login',
            'date_joined',
            'groups',
            'user_permissions',
        )


class UserSignupSerializer(serializers.ModelSerializer):

    passwd_conf = serializers.CharField()

    class Meta:
        model = User

        fields = (
            'password',
            'passwd_conf',
            'first_name',
            'last_name',
            'email',
            'phone',
            'username',
            'image',
        )

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['passwd_conf']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)

        return super().validate(data)

    def create(self, data):
        data.pop('passwd_conf')
        user = User.objects.create_user(**data)
        return user


class UserLoginSerializer(serializers.Serializer):

    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['phone'], password=data['password'])
        if not user:
            raise serializers.ValidationError(
                'Las credenciales no son válidas')

        if not user.is_active:
            raise serializers.ValidationError('user deactivated')

        # Guardar el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return super().validate(data)

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class ChangePasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'image',
                  )


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()