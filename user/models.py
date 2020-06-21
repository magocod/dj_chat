from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.contrib.auth.base_user import BaseUserManager

# from .managers import CustomUserManager


class User(AbstractUser):
    """
    ...
    """

    email = models.EmailField(unique=True)

    # objects = CustomUserManager()
