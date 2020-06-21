"""
Importador usuarios
"""

# standard library
from typing import Any, Dict, Tuple

# Django
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User

# third-party
from rest_framework.authtoken.models import Token

User = get_user_model()

USERS: Tuple[Dict[str, Any]] = (
    {
        "username": "super_user_admin",
        "email": "admin@django.com",
        "password": "123",
        "first_name": "admin",
        "last_name": "Generic",
        "staff": True,
        "super": True,
        "token": "20fd382ed9407b31e1d5f928b5574bb4bffe6120",
    },
    {
        "username": "basic_user",
        "email": "user@django.com",
        "password": "123",
        "first_name": "user",
        "last_name": "Generic",
        "staff": False,
        "super": False,
        "token": "20fd382ed9407b31e1d5f928b5574bb4bffe6130",
    },
    {
        "username": "super_user",
        "email": "superuser@django.com",
        "password": "123",
        "first_name": "super",
        "last_name": "Generic",
        "staff": True,
        "super": True,
        "token": "20fd382ed9407b31e1d5f928b5574bb4bffe6140",
    },
    {
        "username": "user_staff",
        "email": "userstaff@django.com",
        "password": "123",
        "first_name": "staff",
        "last_name": "Generic",
        "staff": True,
        "super": False,
        "token": "20fd382ed9407b31e1d5f928b5574bb4bffe6150",
    },
    {
        "username": "user_staff_2",
        "email": "userstaff2@django.com",
        "password": "123",
        "first_name": "staff",
        "last_name": "Generic",
        "staff": True,
        "super": False,
        "token": "20fd382ed9407b31e1d5f928b5574bb4bffe6160",
    },
)

def user_list():
    """
    migrar en db usuarios con un token
    """
    for values in USERS:
        user = User.objects.create_user(
            values["username"], values["email"], values["password"]
        )
        user.first_name = values["first_name"]
        user.last_name = values["last_name"]
        user.is_staff = values["staff"]
        user.is_superuser = values["super"]
        user.save()
        user = User._default_manager.get_by_natural_key(values["username"])

        tk, _ = Token.objects.get_or_create(user=user)
        # print(token.key)
        # tk.key = values["token"];
        # tk.save()

    print("users created")
