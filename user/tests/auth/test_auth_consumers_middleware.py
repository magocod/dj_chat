"""
authenticacion jwt HS256
"""

import pytest
from channels.testing import WebsocketCommunicator

from django.contrib.auth import get_user_model

from user.consumers.cauth import AuthConsumer

# from django.contrib.auth.models import User

User = get_user_model()

# permitir acceso a db
pytestmark = pytest.mark.django_db


@pytest.mark.asyncio
@pytest.mark.auth_consumer_middleware
async def test_request_auth_token_url(jwt_token):
    """
    ...
    """
    communicator = WebsocketCommunicator(
        AuthConsumer, f"/ws/auth/jwt/{jwt_token['VALID']}/"
    )
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {"data": "data",}
    )
    response = await communicator.receive_json_from()
    assert response == {"data": "data"}
    # assert response == "res"

    # Close
    await communicator.disconnect()


# @pytest.mark.asyncio
# @pytest.mark.auth_consumer_middleware
# async def test_reject_token_request_invalid_url(jwt_token):
#     """
#     ...
#     """
#     communicator = WebsocketCommunicator(
#         AuthConsumer, f"/ws/auth/jwt/{jwt_token['INVALID_FORMAT']}/"
#     )
#     connected, _ = await communicator.connect()

#     assert connected
#     print(communicator.scope)
#     response = await communicator.receive_json_from()
#     response = {"data": "data" }

#     # Close
#     await communicator.disconnect()
