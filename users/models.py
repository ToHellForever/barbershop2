from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомный юзер
    Наследуется от AbstractUser мы получаем все его поля и методы
    И может быть интегрирован с Django гармонично
    """
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    github_id = models.CharField(max_length=255, null=True, blank=True)
