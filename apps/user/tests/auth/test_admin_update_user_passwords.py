"""
Authentication tests
"""

# import json
from typing import Dict

import pytest
from django.contrib.auth import authenticate

pytestmark = [pytest.mark.django_db, pytest.mark.users_credentials]

BASIC_USER: Dict[str, str] = {
    "id": 2,
    "username": "basic_user",
    "password": "123",
}

STAFF_USER: Dict[str, str] = {
    "id": 4,
    "username": "user_staff",
    "password": "123",
}

SUPER_USER: Dict[str, str] = {
    "id": 3,
    "username": "super_user",
    "password": "123",
}


@pytest.mark.auth_update_password
def test_update_the_user_password_with_a_superuser(admin_client):
    """
    ...
    """
    response = admin_client.post(
        "/api/user/password/", {"user_id": BASIC_USER["id"], "password": "1234"}
    )
    assert response.status_code == 200

    user = authenticate(username=BASIC_USER["username"], password="1234",)

    assert user is not None


@pytest.mark.auth_update_password
def test_do_not_allow_to_update_the_password_of_a_superuser(admin_client):
    """
    ...
    """
    response = admin_client.post(
        "/api/user/password/", {"user_id": SUPER_USER["id"], "password": "1234"}
    )
    assert response.status_code == 403
    assert response.data == "editing of superuser passwords is not allowed"

    user = authenticate(username=SUPER_USER["username"], password="1234",)

    assert user is None


@pytest.mark.auth_update_password
def test_edit_the_user_password_that_does_not_exist(admin_client):
    """
    ...
    """
    response = admin_client.post(
        "/api/user/password/", {"user_id": 10000, "password": "1234"}
    )
    assert response.status_code == 404


@pytest.mark.auth_update_password
def test_valid_password_to_update_user_credentials(admin_client):
    """
    ...
    """
    response = admin_client.post("/api/user/password/", {"user_id": 2, "password": ""})
    assert response.status_code == 400
