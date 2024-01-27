from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    nickname = models.CharField('Имя пользователя', max_length=120, default='')
    avatar = models.CharField('Иконка пользователя', max_length=255,
                              default='')  # Создания поля для аватарки пользователя (ссылка)
    user_social = models.CharField('Социальные сети пользователя', max_length=500, default='')
    description = models.TextField('Описания пользователя', default='')

    def __str__(self):
        return self.nickname or ''
