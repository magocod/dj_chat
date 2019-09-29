"""
Prueba creacion de tag
"""

# standard library
# import json
from typing import Dict

# third-party
from rest_framework.test import APIClient

# Django
from django.test import TestCase

# local Django
from apps.tests.auth import create_user

class CRUDTest(TestCase):
    """
    edicion de tag
    """

    def setUp(self) -> None:
        """
        ...
        """
        # user an token
        auth = create_user(True)
        self.public_client = APIClient()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth['token'].key)
        # data

    def test_search_email(self) -> None:
        """
        ...
        """
        data: Dict[str, str] = {
            'email': 'user@test.com',
        }
        response = self.public_client.post('/api/email/', data)
        # print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_email_does_not_exist(self) -> None:
        """
        ...
        """
        data: Dict[str, str] = {
            'email': 'user10@test.com',
        }
        response = self.public_client.post('/api/email/', data)
        # print(response.data)
        self.assertEqual(response.status_code, 404)

    def test_request_token(self) -> None:
        """
        ...
        """
        data: Dict[str, str] = {
            'email': 'user@test.com',
            'password': '123',
        }
        response = self.public_client.post('/api/token-auth/', data)
        # print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_logout(self) -> None:
        """
        ...
        """
        response = self.client.post('/api/user/logout/')
        self.assertEqual(response.status_code, 200)

    def test_repeat_logout(self) -> None:
        """
        ...
        """
        self.client.post('/api/user/logout/')
        response = self.client.post('/api/user/logout/')
        self.assertEqual(response.status_code, 401)
