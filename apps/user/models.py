from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# from django.contrib.auth.base_user import BaseUserManager

# from .managers import CustomUserManager


Group.add_to_class(
    "description", models.CharField(max_length=180, null=True, blank=True)
)


class User(AbstractUser):
    """
    ...
    """

    email = models.EmailField(unique=True)

    # objects = CustomUserManager()
