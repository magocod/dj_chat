"""
Prueba autenticacion
"""

# standard library
# import json
from typing import Dict

# third-party
import pytest

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.users_credentials]


SUPER_USER: Dict[str, str] = {
    "id": 1,
    "username": "super_user_admin",
    "password": "123",
}


@pytest.mark.auth_reset_password
def test_user_reset_password(admin_client):
    """
    ...
    """
    response = admin_client.post(
        "/api/user/reset_password/",
        {"old_password": SUPER_USER["password"], "new_password": "1234"},
    )
    assert response.status_code == 200

    user = authenticate(username=SUPER_USER["username"], password="1234",)

    assert user is not None


@pytest.mark.auth_reset_password
def test_old_error_wrong_password(admin_client):
    """
    ...
    """
    response = admin_client.post(
        "/api/user/reset_password/", {"old_password": "1234", "new_password": "1234"}
    )
    assert response.status_code == 400
    assert response.data == "old password incorrect"

    user = authenticate(username=SUPER_USER["username"], password="1234",)

    assert user is None


@pytest.mark.auth_reset_password
def test_incorrect_user_parameters_to_reset_the_password(admin_client):
    """
    ...
    """
    response = admin_client.post(
        "/api/user/reset_password/", {"old_password": "1234", "password": "1234"}
    )
    assert response.status_code == 400

    user = authenticate(username=SUPER_USER["username"], password="1234",)

    assert user is None
