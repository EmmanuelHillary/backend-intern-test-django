from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=50, verbose_name="Username", blank=True, null=True)
    phone_number = models.CharField(max_length=255, default='')
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.email