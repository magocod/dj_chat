"""
authenticacion jwt HS256
"""


# standard library
import jwt

# import json
# from typing import Dict

# third-party
# import jwt
import pytest

# Django
from django.conf import settings
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# local Django
from user.serializers import UserHeavySerializer

# permitir acceso a db
pytestmark = pytest.mark.django_db

ENCODED = jwt.encode({"some": "payload"}, settings.KEY_HS256, algorithm="HS256")
TEST_JWT_TOKEN = ENCODED.decode("UTF-8")


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
def test_authentiaction_request_failure_keyword():
    """
    ...
    """

    keywordclient = APIClient()
    keywordclient.credentials(HTTP_AUTHORIZATION="Token " + TEST_JWT_TOKEN,)

    response = keywordclient.post("/api/current_user_jwt/")
    assert response.data["detail"] == "Authentication credentials were not provided."
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_token_is_not_in_the_header():
    """
    ...
    """

    keywordclient = APIClient()
    keywordclient.credentials(HTTP_AUTHORIZATION="Bearer ")

    response = keywordclient.post("/api/current_user_jwt/")
    assert response.data["detail"] == "Invalid token header. No credentials provided."
    assert response.status_code == 401


@pytest.mark.auth_jwt_views_authentication
def test_authentiaction_the_token_in_the_header_contains_spaces():
    """
    ...
    """

    keywordclient = APIClient()
    keywordclient.credentials(HTTP_AUTHORIZATION="Bearer " + TEST_JWT_TOKEN + " 12")

    response = keywordclient.post("/api/current_user_jwt/")
    assert (
        response.data["detail"]
        == "Invalid token header. Token string should not contain spaces."
    )
    assert response.status_code == 401


# @pytest.mark.auth_jwt_views_authentication
# def test_get_current_user_jwt(admin_client_jwt):
#     """
#     ...
#     """
#     user = User.objects.get(id=1)
#     user_serializer = UserHeavySerializer(user)
#     # print(user_serializer.data)
#     token, _ = Token.objects.get_or_create(user=user)
#     # print(token)
#     key = settings.KEY_HS256
#     encoded_jwt = jwt.encode(
#         {"token": token.key, "user": user_serializer.data}, key, algorithm="HS256"
#     )
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION="Bearer " + encoded_jwt.decode('UTF-8'),)
