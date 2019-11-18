"""
Prueba autenticacion
"""

# standard library
# import json
from typing import Dict

# third-party
import pytest

# permitir acceso a db
pytestmark = pytest.mark.django_db


@pytest.mark.users_authentication
def test_search_email(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        'email': 'admin@django.com',
    }
    response = public_client.post('/api/email/', data)
    assert response.status_code == 200

@pytest.mark.users_authentication
def test_email_does_not_exist(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        'email': 'user10@test.com',
    }
    response = public_client.post('/api/email/', data)
    assert response.status_code == 404

@pytest.mark.users_authentication
def test_request_token(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        'email': 'admin@django.com',
        'password': '123',
    }
    response = public_client.post('/api/token-auth/', data)
    assert response.status_code == 200

@pytest.mark.users_authentication
def test_logout(admin_client):
    """
    ...
    """
    response = admin_client.post('/api/user/logout/')
    assert response.status_code == 200

@pytest.mark.users_authentication
def test_repeat_logout(public_client):
    """
    ...
    """
    public_client.post('/api/user/logout/')
    response = public_client.post('/api/user/logout/')
    assert response.status_code == 401
