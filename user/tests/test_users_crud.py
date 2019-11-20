"""
Prueba creacion de usuarios
"""

# standard library
# import json
from typing import Dict, Any

# third-party
import pytest

# local Django
from django.contrib.auth.models import User
from user.api.serializers import UserHeavySerializer

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
    response = admin_client.delete('/api/user/' + str(1) + '/')
    assert response.status_code == 204
