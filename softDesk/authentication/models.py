from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Users(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
