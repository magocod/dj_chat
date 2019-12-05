"""
...
"""

# standard library
from typing import Any, Dict

# third-party
import pytest

# Django
# from channels.testing import HttpCommunicator
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

# local Django
from chat.models import Room
from chat.serializers import RoomHeavySerializer
from chat.consumers.croom import RoomConsumer

from tests.db import async_count_db, async_bulk_create_model

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.rooms_consumers]

@database_sync_to_async
def create_event_message(id: int, operation: str) -> Dict[str, Any]:
    room = Room.objects.get(id=id)
    serializer = RoomHeavySerializer(room)
    return {
        'method': operation,
        'data': serializer.data,
    }


@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_create_room():
    """
    ...
    """
    start_rooms: int = await async_count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, '/ws/rooms/')
    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        'method': 'U',
        'values': { 'name': 'YSON' },
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    assert response == await create_event_message(response['data']['id'], 'U')
    
    final_rooms: int = await async_count_db(Room)

    assert start_rooms + 1 == final_rooms
    # Close
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_create_room_error_params():
    """
    ...
    """
    start_rooms: int = await async_count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, '/ws/rooms/')
    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        'method': 'U',
        'values': { 'names': 'YSON' },
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    assert 'errors' in response

    assert start_rooms == await async_count_db(Room)
    # Close
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_delete_room():
    """
    ...
    """

    instances = [
        Room(name=f'name_{number}')
        for number in range(4)
    ]
    await async_bulk_create_model(Room, instances)

    start_rooms: int = await async_count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, '/ws/rooms/')
    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        'method': 'D',
        'values': { 'pk_list': [1, 3] },
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    }
    await communicator.send_json_to(request)

    signal_1 = await communicator.receive_json_from()
    # assert signal_1 == 'yeah'

    signal_2 = await communicator.receive_json_from()
    # assert signal_2 == 'yeah'
    

    response = await communicator.receive_json_from()
    assert response == 'yeah'

    # assert response == {
    #     'count': 2,
    #     'pk_list': [1, 2],
    # }

    assert start_rooms - 2 == await async_count_db(Room)
    # Close
    await communicator.disconnect()
