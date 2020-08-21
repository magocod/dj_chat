"""
...
"""

from typing import Any, Dict

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

from apps.chat.consumers.croom import RoomConsumer
from apps.chat.models import Room
from apps.chat.serializers import RoomHeavySerializer
from tests.db import async_count_db, async_create_model

pytestmark = [pytest.mark.django_db, pytest.mark.rooms_consumers]


@database_sync_to_async
def create_event_message(id: int, operation: str) -> Dict[str, Any]:
    """
    retrieve an element of db
    serialize and return it as a sockect response
    """
    room = Room.objects.get(id=id)
    serializer = RoomHeavySerializer(room)
    return {
        "method": operation,
        "data": serializer.data,
    }


@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_create_room(auth_token):
    """
    ...
    """
    start_rooms: int = await async_count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        "method": "U",
        "values": {"name": "YSON"},
        "token": auth_token["super_user_admin"],
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    assert response == await create_event_message(
        id=response["data"]["id"], operation="U",
    )

    final_rooms: int = await async_count_db(Room)

    assert start_rooms + 1 == final_rooms
    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_update_room(auth_token):
    """
    ...
    """
    init_room = await async_create_model(Room, name="YSONS")
    init_serializer = RoomHeavySerializer(init_room).data
    start_rooms: int = await async_count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        "method": "U",
        "values": {"name": "YSONS"},
        "token": auth_token["super_user_admin"],
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    assert response == await create_event_message(
        id=response["data"]["id"], operation="U",
    )
    assert response["data"] != init_serializer

    assert start_rooms == await async_count_db(Room)
    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_create_room_error_params(auth_token):
    """
    ...
    """
    start_rooms: int = await async_count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        "method": "U",
        "values": {"names": "YSON"},
        "token": auth_token["super_user_admin"],
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    assert "errors" in response

    assert start_rooms == await async_count_db(Room)
    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_consumer_delete_room(auth_token):
    """
    each elimination triggers signal
    that is sent to all active consumers
    """
    start_rooms: int = await async_count_db(Room)

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        "method": "D",
        "values": {"pk_list": [3, 4]},
        "token": auth_token["super_user_admin"],
    }

    # deleted_signal_1 = await create_event_message(
    #     id=3,
    #     operation='D',
    # )
    # deleted_signal_2 = await create_event_message(
    #     id=4,
    #     operation='D',
    # )

    # 2 signals and the answer
    await communicator.send_json_to(request)

    # await communicator.receive_json_from()
    # signal_1 = await communicator.receive_json_from()
    # assert signal_1 == deleted_signal_1 or signal_1 == deleted_signal_2

    # await communicator.receive_json_from()
    # signal_2 = await communicator.receive_json_from()
    # assert signal_2 == deleted_signal_1 or signal_2 == deleted_signal_2

    # await communicator.receive_json_from()
    response = await communicator.receive_json_from()
    # assert response == 'yeah'
    # print(response)
    assert response == {
        "method": "D",
        "data": {"count": 2, "pk_list": [3, 4],},
    }

    assert start_rooms - 2 == await async_count_db(Room)
    # Close
    await communicator.disconnect()
