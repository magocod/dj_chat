"""
user tests edit profile
"""

# standard library
# import json
from typing import Any, Dict

# third-party
import pytest

from django.contrib.auth import get_user_model
from apps.user.serializers import UserHeavySerializer

# local Django
# from django.contrib.auth.models import User

User = get_user_model()


# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.users_views]


@pytest.mark.users_profile
def test_user_update_profile(admin_client):
    """
    ...
    """
    user_id: int = 1
    oldvalues = UserHeavySerializer(User.objects.get(id=user_id))
    newdata: Dict[str, Any] = {
        "username": "NEW",
        "first_name": "new name",
        "last_name": "new name2",
        "email": "newemail@django.com",
    }
    response = admin_client.post("/api/user/profile/", newdata)
    newvalues = UserHeavySerializer(User.objects.get(id=user_id))
    assert response.status_code == 200
    assert newvalues.data != oldvalues.data
    assert newvalues.data == response.data


@pytest.mark.users_profile
def test_user_update_profile_invalid_params(admin_client):
    """
    ...
    """
    user_id: int = 1
    oldvalues = UserHeavySerializer(User.objects.get(id=user_id))
    newdata: Dict[str, Any] = {
        "usernames": "NEW",
        "first_names": "new name",
    }
    response = admin_client.post("/api/user/profile/", newdata)
    newvalues = UserHeavySerializer(User.objects.get(id=user_id))
    assert response.status_code == 400
    assert newvalues.data == oldvalues.data


@pytest.mark.users_profile
def test_get_current_auth_user(admin_client):
    """[summary]

    [description]

    Decorators:
        pytest.mark.users_profile

    Arguments:
        admin_client {[type]} -- [description]
    """
    user_serializer = UserHeavySerializer(User.objects.get(id=1))

    response = admin_client.get("/api/user/profile/")
    # assert response.data == 'si'
    assert response.status_code == 200
    assert response.data == user_serializer.data


@pytest.mark.users_profile
def test_get_current_auth_user_failed(public_client):
    """[summary]

    [description]

    Decorators:
        pytest.mark.users_profile

    Arguments:
        public_client {[type]} -- [description]
    """

    response = public_client.get("/api/user/profile/")
    # assert response.data == 'si'
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."
