from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Юзернейм',
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name='Почта'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default=USER,
        verbose_name='Статус'
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
