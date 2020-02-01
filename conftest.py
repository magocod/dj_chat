"""
Ajustes pruebas
"""

# third-party
import pytest
# Django
from django.core.management import call_command
from rest_framework.test import APIClient


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Cargar bd de prueba
    """
    with django_db_blocker.unblock():
        call_command('default_db')
        call_command('chat_example_db')


@pytest.fixture
def admin_client():
    """
    super user
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Token '
        + '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    )
    return client


@pytest.fixture
def user_client():
    """
    basic user
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Token '
        + '20fd382ed9407b31e1d5f928b5574bb4bffe6130',
    )
    return client


@pytest.fixture
def staff_client():
    """
    basic admin user
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Token '
        + '20fd382ed9407b31e1d5f928b5574bb4bffe6150',
    )
    return client


@pytest.fixture
def false_client():
    """
    user invalid token
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Token '
        + '123',
    )
    return client


@pytest.fixture
def public_client():
    """
    user not authenticated
    """
    client = APIClient()
    return client
