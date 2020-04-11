"""
Ajustes pruebas
"""

# third-party
import jwt
import pytest
from rest_framework.authtoken.models import Token

# Django
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APIClient

# local Django
from user.serializers import UserHeavySerializer


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Cargar bd de prueba
    """
    with django_db_blocker.unblock():
        call_command("default_db")
        call_command("chat_example_db")


@pytest.fixture
def admin_client():
    """
    super user
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION="Token " + "20fd382ed9407b31e1d5f928b5574bb4bffe6120",
    )
    return client


@pytest.fixture
def user_client():
    """
    basic user
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION="Token " + "20fd382ed9407b31e1d5f928b5574bb4bffe6130",
    )
    return client


@pytest.fixture
def staff_client():
    """
    basic admin user
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION="Token " + "20fd382ed9407b31e1d5f928b5574bb4bffe6150",
    )
    return client


@pytest.fixture
def false_client():
    """
    user invalid token
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + "123",)
    return client


@pytest.fixture
def public_client():
    """
    user not authenticated
    """
    client = APIClient()
    return client


@pytest.fixture
def admin_client_jwt():
    """
    user jwt authenticated
    """
    user = User.objects.get(id=1)
    user_serializer = UserHeavySerializer(user)
    # print(user_serializer.data)
    token, _ = Token.objects.get_or_create(user=user)
    # print(token)
    key = settings.KEY_HS256
    encoded_jwt = jwt.encode(
        {"token": token.key, "user": user_serializer.data}, key, algorithm="HS256"
    )
    # print(type(encoded_jwt))
    # print(encoded_jwt.decode('UTF-8'))
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + encoded_jwt.decode('UTF-8'),)
    return client
