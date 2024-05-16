from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='Контактный номер', **NULLABLE)
    token = models.CharField(max_length=50, verbose_name='Токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('set_is_active', 'Активация пользователя')
        ]
