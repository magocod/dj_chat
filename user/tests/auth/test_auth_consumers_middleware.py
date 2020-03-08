"""
authenticacion jwt HS256
"""

# standard library
# import json
# from typing import Dict

# third-party
import jwt
import pytest
from channels.testing import WebsocketCommunicator

# Django
from django.conf import settings

# local Django
from user.consumers.cauth import AuthConsumer

# from django.contrib.auth.models import User


# permitir acceso a db
pytestmark = pytest.mark.django_db

VALID_ENCODED = jwt.encode(
    {"token": "20fd382ed9407b31e1d5f928b5574bb4bffe6120", "user": None},
    settings.KEY_HS256,
    algorithm="HS256",
)

INVALID_ENCODED = jwt.encode(
    {"token": "123", "user": None}, settings.KEY_HS256, algorithm="HS256"
)


@pytest.mark.asyncio
@pytest.mark.auth_consumer_middleware
async def test_request_auth_token_url():
    """
    ...
    """
    communicator = WebsocketCommunicator(AuthConsumer, f"/ws/auth/jwt/{VALID_ENCODED}/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {"data": "data",}
    )
    await communicator.receive_json_from()

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.auth_consumer_middleware
async def test_reject_token_request_invalid_url():
    """
    ...
    """
    communicator = WebsocketCommunicator(
        AuthConsumer, f"/ws/auth/jwt/{INVALID_ENCODED}/"
    )
    connected, _ = await communicator.connect()

    assert connected

    # Close
    await communicator.disconnect()
