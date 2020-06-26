"""
Prueba autenticacion
"""

# standard library
# import json
from typing import Dict

# third-party
import pytest

from django.contrib.auth import get_user_model

# from django.contrib.auth.models import User


User = get_user_model()


# permitir acceso a db
pytestmark = pytest.mark.django_db


@pytest.mark.users_authentication
def test_search_email(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "email": "admin@django.com",
    }
    response = public_client.post("/api/email/", data)
    assert response.status_code == 200


@pytest.mark.users_authentication
def test_email_does_not_exist(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "email": "user10@test.com",
    }
    response = public_client.post("/api/email/", data)
    assert response.status_code == 404


@pytest.mark.users_authentication
def test_invalid_search_email_params(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "emails": "novalid@django.com",
    }
    response = public_client.post("/api/email/", data)
    assert response.status_code == 400


@pytest.mark.users_authentication
def test_success_request_token(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "email": "admin@django.com",
        "password": "123",
    }
    response = public_client.post("/api/token-auth/", data)
    assert response.status_code == 200


@pytest.mark.users_authentication
def test_error_credentials(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "e": "notexist@django.com",
        "pass": "123",
    }
    response = public_client.post("/api/token-auth/", data)
    assert response.status_code == 400


@pytest.mark.users_authentication
def test_error_user_account_is_disabled(public_client):
    """
    ...
    """
    User.objects.filter(id=1).update(is_active=False)
    data: Dict[str, str] = {
        "email": "admin@django.com",
        "password": "123",
    }
    response = public_client.post("/api/token-auth/", data)
    assert response.status_code == 400
    assert response.data["non_field_errors"][0] == "User account is disabled."


@pytest.mark.users_authentication
def test_error_user_not_exist(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "email": "notexist@django.com",
        "password": "123",
    }
    response = public_client.post("/api/token-auth/", data)
    assert response.status_code == 400
    assert response.data["non_field_errors"][0] == "User no exist."


@pytest.mark.users_authentication
def test_error_invalid_password(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "email": "admin@django.com",
        "password": "novalid",
    }
    response = public_client.post("/api/token-auth/", data)
    assert response.status_code == 400
    # print(response.data)
    assert (
        response.data["non_field_errors"][0]
        == "Unable to log in with provided credentials."
    )


@pytest.mark.users_authentication
def test_logout(admin_client):
    """
    ...
    """
    response = admin_client.post("/api/user/logout/")
    assert response.status_code == 200


@pytest.mark.users_authentication
def test_repeat_logout(public_client):
    """
    ...
    """
    public_client.post("/api/user/logout/")
    response = public_client.post("/api/user/logout/")
    assert response.status_code == 401


@pytest.mark.users_authentication
def test_logout_invalid_token(false_client):
    false_client.post("/api/user/logout/")
    response = false_client.post("/api/user/logout/")
    assert response.status_code == 401
