"""
Authentication jwt HS256
"""

# import json
from typing import Dict

import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from apps.user.serializers import UserHeavySerializer

pytestmark = pytest.mark.django_db


User = get_user_model()


@pytest.mark.auth_jwt_hs256
def test_success_login_jwt(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "email": "admin@django.com",
        "password": "123",
    }
    response = public_client.post("/api/jwt-auth/", data)
    assert response.status_code == 200

    decoded = jwt.decode(response.data, settings.KEY_HS256, algorithms="HS256")
    user = User.objects.get(email=data["email"])
    serialer = UserHeavySerializer(user)
    token = Token.objects.get(user_id=user.id)

    assert decoded["token"] == token.key
    assert decoded["user"] == serialer.data


@pytest.mark.auth_jwt_hs256
def test_failed_login_jwt(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        "email": "noexist@django.com",
        "password": "123",
    }
    response = public_client.post("/api/jwt-auth/", data)
    assert response.status_code == 422
