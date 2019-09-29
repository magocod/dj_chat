"""
Prueba creacion de usuarios
"""

# standard library
import json
from typing import Dict, Any

# third-party
from rest_framework.test import APIClient

# Django
from django.test import TestCase

# local Django
from django.contrib.auth.models import User
from apps.user.serializers import UserHeavySerializer
from apps.tests.auth import create_user

class CRUDTest(TestCase):
    """
    edicion de usuarios
    """
    serializer = UserHeavySerializer

    def setUp(self) -> None:
        """
        ...
        """
        # user an token
        auth = create_user(True)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth['token'].key)
        # data

    def test_create_user(self) -> None:
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
        response = self.client.post('/api/users/', data)
        response_data = json.loads(response.content)
        serializer = self.serializer(
            User.objects.get(id=response_data['id']),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(serializer.data, response_data)

    def test_create_error_params(self):
        """
        ...
        """
        data: Dict[str, Any] = {
            'names': 'NEW_USER',
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, 400)

    def test_create_error_duplicate(self):
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
        self.client.post('/api/users/', data)
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        """
        ...
        """
        response = self.client.get('/api/user/' + str(1) + '/')
        serializer = self.serializer(
            User.objects.get(id=1)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)

    def test_update_user(self):
        """
        ...
        """
        oldvalues = self.serializer(User.objects.get(id=1))
        newdata: Dict[str, Any] = {
            'username': 'NEW',
            'first_name': 'new name',
            'last_name': 'new name2',
        }
        response = self.client.put('/api/user/' + str(1) + '/', newdata)
        newvalues = self.serializer(User.objects.get(id=1))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(newvalues.data, oldvalues.data)
        self.assertEqual(newvalues.data, response.data)

    def test_delete_user(self):
        """
        ...
        """
        response = self.client.delete('/api/user/' + str(1) + '/')
        self.assertEqual(response.status_code, 204)
