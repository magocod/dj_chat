"""
...
"""

# standard library
# from typing import Any, Dict

# third-party
import pytest
from channels.testing import WebsocketCommunicator
# local Django
from chat.consumers.cmessage import MessageConsumer
from chat.models import Message
from chat.serializers import MessageHeavySerializer

from tests.db import async_count_db  # async_create_model,
from tests.db import async_count_filter_db, async_delete_models
from tests.response import create_event_message

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.messages_consumers]


@pytest.mark.asyncio
@pytest.mark.messages_crud
async def test_consumer_create_message_in_room(auth_token):
    """
    ...
    """
    start_messages_count: int = await async_count_db(Message)
    start_messages_count_room: int = await async_count_filter_db(
        Message, room_id=3,
    )

    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # join chat room 3
    await communicator.send_json_to(
        {
            "method": "J",
            "values": {"room_id": 3},
            "token": auth_token["super_user_admin"],
        }
    )

    await communicator.send_json_to(
        {
            "method": "C",
            "values": {"text": "hello", "room_id": 3,},
            "token": auth_token["super_user_admin"],
        }
    )

    await communicator.receive_json_from()
    # notify_user = await communicator.receive_json_from()
    await communicator.receive_json_from()
    # notify_group = await communicator.receive_json_from()
    response = await communicator.receive_json_from()
    # print('1', notify_user)
    # print('2', notify_group)
    # print('3', response)
    assert response == await create_event_message(
        id=response["data"]["id"],
        operation="C",
        model=Message,
        serializer=MessageHeavySerializer,
    )

    assert start_messages_count + 1 == await async_count_db(Message)
    assert start_messages_count_room + 1 == await async_count_filter_db(
        Message, room_id=3,
    )

    # Close
    await async_delete_models(Message, id=response["data"]["id"])
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_crud
async def test_consumer_create_message_in_non_existent_room(auth_token):
    """
    ...
    """
    start_messages_count: int = await async_count_db(Message)

    communicator_n = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_n.connect()
    assert connected

    await communicator_n.send_json_to(
        {
            "method": "C",
            "values": {"text": "hello", "room_id": 100,},
            "token": auth_token["super_user_admin"],
        }
    )
    # await communicator_n.receive_json_from()
    response = await communicator_n.receive_json_from()
    # assert response == 'y'
    assert "errors" in response

    assert start_messages_count == await async_count_db(Message)

    # Close
    await communicator_n.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_crud
async def test_consumer_delete_message_in_room(auth_token):
    """
    ...
    """
    start_messages_count: int = await async_count_db(Message)
    start_messages_count_room: int = await async_count_filter_db(
        Message, room_id=1,
    )
    expected_response = await create_event_message(
        id=1, operation="D", model=Message, serializer=MessageHeavySerializer,
    )

    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # join chat room
    await communicator.send_json_to(
        {
            "method": "J",
            "values": {"room_id": 1},
            "token": auth_token["super_user_admin"],
        }
    )

    await communicator.send_json_to(
        {
            "method": "D",
            "values": {"message_id": 1,},
            "token": auth_token["super_user_admin"],
        }
    )

    # join group notify user
    await communicator.receive_json_from()
    # join group motify group
    await communicator.receive_json_from()
    assert expected_response == await communicator.receive_json_from()

    assert start_messages_count - 1 == await async_count_db(Message)
    assert start_messages_count_room - 1 == await async_count_filter_db(
        Message, room_id=1,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_crud
async def test_consumer_delete_message_that_does_not_exist(auth_token):
    """
    ...
    """
    start_messages_count: int = await async_count_db(Message)

    communicator_n = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_n.connect()
    assert connected

    await communicator_n.send_json_to(
        {
            "method": "D",
            "values": {"message_id": 100,},
            "token": auth_token["super_user_admin"],
        }
    )
    # await communicator_n.receive_json_from()
    response = await communicator_n.receive_json_from()
    # assert response == 'y'
    assert "errors" in response

    assert start_messages_count == await async_count_db(Message)

    # Close
    await communicator_n.disconnect()
