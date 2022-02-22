from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    telephone_number = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'username', 'telephone_number', 'password', 'token', 'access', 'refresh']

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    telephone_number = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Нужны почта или логин, чтобы войти'
            )

        if password is None:
            raise serializers.ValidationError(
                'Нужен пароль, чтобы войти'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            try:
                user = User.objects.filter(username=email)
                email = user[0]
                user = authenticate(username=email, password=password)
                if user is None:
                    raise serializers.ValidationError(
                        'Данные указаны неверно'
                    )
            except Exception:
                raise serializers.ValidationError(
                    'Данные указаны неверно'
                )

        if not user.is_active:
            raise serializers.ValidationError(
                'Пользователь был деактивирован'
            )

        if not user.verified and not user.vk and not user.google:
            raise serializers.ValidationError(
                'Вы не подтвердили почту'
            )

        return {
            'email': user.email,
            'username': user.username,
            'telephone_number': user.telephone_number,
            'access': user.token['access'],
            'refresh': user.token['refresh']
        }


class UserSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов User. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', 'telephone_number', 'vk', 'google')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """

        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class CodeCheckSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['code']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise serializers.ValidationError(
                'Токен устарел или неверен'
            )


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data['refresh'] = str(refresh)

        return data


class VkSerializer(serializers.Serializer):
    vk = serializers.CharField(max_length=255)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        vk = data.get('vk', '')
        user = User.objects.get(vk=vk)
        return {
            'vk': vk,
            'access': user.token['access'],
            'refresh': user.token['refresh']
        }


class GoogleSerializer(serializers.Serializer):
    google = serializers.CharField(max_length=255)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        google = data.get('google', '')
        user = User.objects.get(google=google)
        return {
            'google': google,
            'access': user.token['access'],
            'refresh': user.token['refresh']
        }
