"""
...
"""

# standard library

# third-party
import pytest

# Django
# from channels.testing import HttpCommunicator
from channels.testing import WebsocketCommunicator

# local Django
from chat.models import Room
from chat.consumers.croom import RoomConsumer

from tests.db import count_db

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.rooms_consumers]


@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_create_room():
    """
    ...
    """
    start_rooms: int = await count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, '/ws/rooms/')
    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        'method': 'c',
        'values': { 'name': 'YSON' },
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    assert response == 'yeah'
    
    final_rooms: int = await count_db(Room)

    assert start_rooms + 1 == final_rooms
    # Close
    await communicator.disconnect()
