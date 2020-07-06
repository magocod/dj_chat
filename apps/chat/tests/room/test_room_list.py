"""
...
"""

import pytest
from channels.testing import WebsocketCommunicator

from apps.chat.consumers.croom import RoomConsumer
from apps.chat.models import Room
from apps.chat.serializers import RoomHeavySerializer
from tests.response import create_event_list_message

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.rooms_consumers]


@pytest.mark.asyncio
@pytest.mark.rooms_list
async def test_consumer_room_list(auth_token):
    """
    ...
    """

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {
            "method": "R",
            "values": {"name": "YSON"},
            "token": auth_token["super_user_admin"],
        }
    )

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert response == await create_event_list_message(
        model=Room, serializer=RoomHeavySerializer,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.rooms_list
async def test_consumer_room_invalid_operation(auth_token):
    """
    ...
    """
    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        "method": "H",
        "values": {"name": "YSON"},
        "token": auth_token["super_user_admin"],
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert "errors" in response

    # Close
    await communicator.disconnect()
