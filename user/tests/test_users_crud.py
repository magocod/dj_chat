"""
Prueba creacion de usuarios
"""

# standard library
# import json
from typing import Any, Dict

# third-party
import pytest
# local Django
from django.contrib.auth.models import User

from user.serializers import UserHeavySerializer

# permitir acceso a db
pytestmark = pytest.mark.django_db


@pytest.mark.users_views
def test_create_user(admin_client):
    """
    ...
    """
    data: Dict[str, Any] = {
        'username': 'NEW',
        'email': 'newemail@gmail.com',
        'password': '123',
        'first_name': 'name',
        'last_name': 'name2',
        'is_staff': False,
    }
    response = admin_client.post('/api/users/', data)
    serializer = UserHeavySerializer(
        User.objects.get(id=response.data['id']),
    )
    assert response.status_code == 201
    assert serializer.data == response.data


@pytest.mark.users_views
def test_not_allowed_to_create_user(user_client, public_client):
    """
    ...
    """
    data: Dict[str, Any] = {
        'username': 'NEW',
        'email': 'newemail@gmail.com',
        'password': '123',
        'first_name': 'name',
        'last_name': 'name2',
        'is_staff': False,
    }
    response = user_client.post('/api/users/', data)
    assert response.status_code == 403
    response = public_client.post('/api/users/', data)
    assert response.status_code == 401


@pytest.mark.users_views
def test_not_create_superuser(admin_client):
    """
    ...
    """
    data: Dict[str, Any] = {
        'username': 'superuser',
        'email': 'newsuperemail@gmail.com',
        'password': '123',
        'first_name': 'name',
        'last_name': 'name2',
        'is_staff': True,
        'is_superuser': True,
    }
    response = admin_client.post('/api/users/', data)
    serializer = UserHeavySerializer(
        User.objects.get(id=response.data['id']),
    )
    assert response.status_code == 201
    assert response.data == serializer.data
    assert not response.data['is_superuser']


@pytest.mark.users_views
def test_create_error_params(admin_client):
    """
    ...
    """
    data: Dict[str, Any] = {
        'names': 'NEW_USER',
        'email': 'newemail@gmail.com',
    }
    response = admin_client.post('/api/users/', data)
    assert response.status_code == 400


@pytest.mark.users_views
def test_create_error_duplicate(admin_client):
    """
    ...
    """
    data: Dict[str, Any] = {
        'username': 'NEW',
        'email': 'newemail@gmail.com',
        'password': '123',
        'first_name': 'name',
        'last_name': 'name2',
        'is_staff': False,
    }
    admin_client.post('/api/users/', data)
    response = admin_client.post('/api/users/', data)
    assert response.status_code == 400


@pytest.mark.users_views
def test_get_user(admin_client):
    """
    ...
    """
    response = admin_client.get('/api/user/' + str(1) + '/')
    serializer = UserHeavySerializer(
        User.objects.get(id=1)
    )
    assert response.status_code == 200
    assert serializer.data == response.data


@pytest.mark.users_views
def test_get_user_not_found(admin_client):
    """
    ...
    """
    response = admin_client.get('/api/user/' + str(1000) + '/')
    assert response.status_code == 404


@pytest.mark.users_views
def test_update_user(admin_client):
    """
    ...
    """
    oldvalues = UserHeavySerializer(User.objects.get(id=1))
    newdata: Dict[str, Any] = {
        'username': 'NEW',
        'first_name': 'new name',
        'last_name': 'new name2',
    }
    response = admin_client.put('/api/user/' + str(1) + '/', newdata)
    newvalues = UserHeavySerializer(User.objects.get(id=1))
    assert response.status_code == 200
    assert newvalues.data != oldvalues.data
    assert newvalues.data == response.data


@pytest.mark.users_views
def test_delete_user(admin_client):
    """
    ...
    """
    response = admin_client.delete('/api/user/' + str(2) + '/')
    assert response.status_code == 204


@pytest.mark.users_views
def test_not_allowed_to_delete_user(user_client, public_client):
    """
    ...
    """
    response = user_client.delete('/api/user/' + str(4) + '/')
    assert response.status_code == 403
    response = public_client.delete('/api/user/' + str(4) + '/')
    assert response.status_code == 401


@pytest.mark.users_views
def test_user_does_not_delete_himself(admin_client):
    """
    ...
    """
    response = admin_client.delete('/api/user/' + str(1) + '/')
    assert response.status_code == 400
    assert response.data == "can't delete himself"


@pytest.mark.users_views
def test_not_delete_superuser(admin_client):
    """
    ...
    """
    response = admin_client.delete('/api/user/' + str(3) + '/')
    assert response.status_code == 400
    assert response.data == 'super users cannot be deleted'


@pytest.mark.users_views
def test_delete_admin_user(admin_client, staff_client):
    """
    ...
    """
    response = staff_client.delete('/api/user/' + str(5) + '/')
    assert response.status_code == 400
    assert response.data == 'user cannot delete administrators'
    response = admin_client.delete('/api/user/' + str(5) + '/')
    assert response.status_code == 204
