from os import path

from django.contrib.postgres.fields import ArrayField
from django.db import models
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, username, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True, null=True)
    email = models.EmailField(db_index=True, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    telephone_number = models.CharField(max_length=16, blank=True, default="", null=True)
    array_of_pages = ArrayField(default=list, null=True, base_field=models.CharField(max_length=10, null=True))
    vk = models.CharField(default='', max_length=20, null=True, blank=True)
    access_vk = models.CharField(default='', max_length=256, null=True, blank=True)
    google = models.CharField(default='', max_length=30, null=True, blank=True)
    access_google = models.CharField(default='', max_length=256, null=True, blank=True)
    allow_promotion = models.BooleanField(default=True)
    allow_useful_information = models.BooleanField(default=True)
    allow_new_things = models.BooleanField(default=True)
    allow_suspicious = models.BooleanField(default=True)
    allow_unidentified = models.BooleanField(default=True)
    remind_after = models.IntegerField(default=3)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_tokens()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Register(models.Model):
    email = models.EmailField('Почта')
    hash = models.CharField('Хэш', max_length=50, blank=True)
    user_id = models.IntegerField()

    def __str__(self):
        return self.email
