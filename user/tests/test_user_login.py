"""
Prueba autenticacion
"""

# standard library
# import json
from typing import Dict

# third-party
import pytest


@pytest.mark.users_authentication
def test_search_email(public_client):
    """
    ...
    """
    data: Dict[str, str] = {
        'email': 'admin@django.com',
    }
    response = public_client.post('/api/email/', data)
    assert response.status_code == 200

    # def test_email_does_not_exist(self) -> None:
    #     """
    #     ...
    #     """
    #     data: Dict[str, str] = {
    #         'email': 'user10@test.com',
    #     }
    #     response = self.public_client.post('/api/email/', data)
    #     # print(response.data)
    #     self.assertEqual(response.status_code, 404)

    # def test_request_token(self) -> None:
    #     """
    #     ...
    #     """
    #     data: Dict[str, str] = {
    #         'email': 'user@test.com',
    #         'password': '123',
    #     }
    #     response = self.public_client.post('/api/token-auth/', data)
    #     # print(response.data)
    #     self.assertEqual(response.status_code, 200)

    # def test_logout(self) -> None:
    #     """
    #     ...
    #     """
    #     response = self.client.post('/api/user/logout/')
    #     self.assertEqual(response.status_code, 200)

    # def test_repeat_logout(self) -> None:
    #     """
    #     ...
    #     """
    #     self.client.post('/api/user/logout/')
    #     response = self.client.post('/api/user/logout/')
    #     self.assertEqual(response.status_code, 401)