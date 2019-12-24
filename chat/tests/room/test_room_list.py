"""
...
"""

# standard library
from typing import Any, Dict

# third-party
import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

from chat.consumers.croom import RoomConsumer
# local Django
from chat.models import Room
from chat.serializers import RoomHeavySerializer
from tests.db import (
    async_count_db,
)
from tests.response import create_event_list_message

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.rooms_consumers]


@pytest.mark.asyncio
@pytest.mark.rooms_list
async def test_consumer_list_room():
    """
    ...
    """
    communicator = WebsocketCommunicator(RoomConsumer, '/ws/rooms/')
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to({
        'method': 'R',
        'values': {'name': 'YSON'},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert response == await create_event_list_message(
        model=Room,
        serializer=RoomHeavySerializer,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.rooms_list
async def test_consumer_invalid_operation():
    """
    ...
    """
    communicator = WebsocketCommunicator(RoomConsumer, '/ws/rooms/')
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        'method': 'H',
        'values': {'name': 'YSON'},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert 'errors' in response

    # Close
    await communicator.disconnect()
