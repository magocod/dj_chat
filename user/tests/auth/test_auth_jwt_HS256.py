"""
authenticacion jwt HS256
"""


# standard library
# import json
from typing import Dict

# third-party
import jwt
import pytest
from rest_framework.authtoken.models import Token

# Django
from django.conf import settings
from django.contrib.auth.models import User

# local Django
from user.serializers import UserHeavySerializer

# permitir acceso a db
pytestmark = pytest.mark.django_db


@pytest.mark.auth_jwt_hs256
def test_success_request_jwt(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        'email': 'admin@django.com',
        'password': '123',
    }
    response = public_client.post('/api/jwt-auth/', data)
    assert response.status_code == 200

    decoded = jwt.decode(
        response.data,
        settings.KEY_HS256,
        algorithms='HS256'
    )
    user = User.objects.get(email=data['email'])
    serialer = UserHeavySerializer(
        user
    )
    token = Token.objects.get(user_id=user.id)

    assert decoded['token'] == token.key
    assert decoded['user'] == serialer.data


@pytest.mark.auth_jwt_hs256
def test_failed_request_jwt(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        'email': 'noexist@django.com',
        'password': '123',
    }
    response = public_client.post('/api/jwt-auth/', data)
    assert response.status_code == 400
