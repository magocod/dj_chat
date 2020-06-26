"""
authenticacion jwt HS256
"""


# standard library
import jwt

# third-party
# import jwt
import pytest

# Django
from django.conf import settings
from django.contrib.auth import get_user_model

# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# local Django
from user.serializers import UserHeavySerializer

# import json
# from typing import Dict

User = get_user_model()

# permitir acceso a db
pytestmark = pytest.mark.django_db

ENCODED_VALID = jwt.encode(
    {"token": "20fd382ed9407b31e1d5f928b5574bb4bffe6120", "user": {}},
    settings.KEY_HS256,
    algorithm="HS256",
)
ENCODED_KEY = jwt.encode({"some": "payload"}, "invalid", algorithm="HS256")
ENCODED_CONTENT_TOKEN = jwt.encode(
    {"token": "20fd382ed9407b31e1d5f928b5574bb4bffe6120"},
    settings.KEY_HS256,
    algorithm="HS256",
)
ENCODED_CONTENT_USER = jwt.encode({"user": {}}, settings.KEY_HS256, algorithm="HS256")

JWT = ENCODED_VALID.decode("UTF-8")
JWT_INVALID_KEY = ENCODED_KEY.decode("UTF-8")
JWT_INVALID_TOKEN = ENCODED_CONTENT_USER.decode("UTF-8")
JWT_INVALID_USER = ENCODED_CONTENT_TOKEN.decode("UTF-8")


@pytest.mark.auth_jwt_views_authentication
def test_get_current_user_jwt(admin_client_jwt):
    """
    admin_client_jwt -> user id: 1
    """
    user_serializer = UserHeavySerializer(User.objects.get(id=1))

    response = admin_client_jwt.post("/api/current_user_jwt/")
    # assert response.data == 'si'
    assert response.status_code == 200
    assert response.data == user_serializer.data


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_request_failure_keyword(jwt_token):
    """
    ...
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + jwt_token['VALID'],)

    response = client.post("/api/current_user_jwt/")
    assert response.data["detail"] == "Authentication credentials were not provided."
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_jwt_key_invalidates(jwt_token):
    """
    ...
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token['INVALID_KEY']}")

    response = client.post("/api/current_user_jwt/")
    assert response.data["detail"] == "Signature verification failed"
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_token_is_not_in_the_header():
    """
    ...
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer ")

    response = client.post("/api/current_user_jwt/")
    assert response.data["detail"] == "Invalid token header. No credentials provided."
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_the_token_in_the_header_contains_spaces(jwt_token):
    """
    ...
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token['VALID'] + " 12")

    response = client.post("/api/current_user_jwt/")
    assert (
        response.data["detail"]
        == "Invalid token header. Token string should not contain spaces."
    )
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_no_user_token_after_jwt_decoding(jwt_token):
    """
    ...
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token['INVALID_TOKEN'])

    response = client.post("/api/current_user_jwt/")
    assert response.data["detail"] == "invalid decoded token (token)"
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_no_user_after_jwt_decoding(jwt_token):
    """
    ...
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token['INVALID_USER'])

    response = client.post("/api/current_user_jwt/")
    assert response.data["detail"] == "invalid decoded token (user)"
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_the_user_in_jwt_is_disabled(jwt_token):
    """
    ...
    """

    User.objects.filter(id=1).update(is_active=False)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token['VALID']}")

    response = client.post("/api/current_user_jwt/")
    assert response.data["detail"] == "User inactive or deleted."
    assert response.status_code == 401
