"""
...
"""

# standard library
# from typing import Any, Dict

# third-party
import pytest
from channels.testing import WebsocketCommunicator

from chat.consumers.cmessage import MessageConsumer
# local Django
from chat.models import Message
from chat.serializers import MessageHeavySerializer
from tests.db import (
    # async_create_model,
    async_count_db,
    async_count_filter_db,
)
from tests.response import create_event_message

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.messages_consumers]


@pytest.mark.asyncio
@pytest.mark.messages_crud
async def test_consumer_create_message_in_room():
    """
    ...
    """
    start_messages_count: int = await async_count_db(Message)
    start_messages_count_room: int = await async_count_filter_db(
        Message,
        room_id=3,
    )

    communicator = WebsocketCommunicator(MessageConsumer, '/ws/chat/')
    connected, _ = await communicator.connect()
    assert connected

    # join chat room 3
    await communicator.send_json_to({
        'method': 'J',
        'values': {'room_id': 3},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })
    await communicator.receive_json_from()

    await communicator.send_json_to({
        'method': 'C',
        'values': {
            'text': 'hello',
            'room_id': 3,
        },
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })
    # await communicator.receive_json_from()
    response = await communicator.receive_json_from()
    assert response == await create_event_message(
        id=response['data']['id'],
        operation='C',
        model=Message,
        serializer=MessageHeavySerializer,
    )

    assert start_messages_count + 1 == await async_count_db(Message)
    assert start_messages_count_room + 1 == await async_count_filter_db(
        Message,
        room_id=3,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_crud
async def test_consumer_delete_message_in_room():
    """
    ...
    """
    start_messages_count: int = await async_count_db(Message)
    start_messages_count_room: int = await async_count_filter_db(
        Message,
        room_id=1,
    )
    expected_response = await create_event_message(
        id=1,
        operation='D',
        model=Message,
        serializer=MessageHeavySerializer,
    )

    communicator = WebsocketCommunicator(MessageConsumer, '/ws/chat/')
    connected, _ = await communicator.connect()
    assert connected

    # join chat room 3
    await communicator.send_json_to({
        'method': 'J',
        'values': {'room_id': 1},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })
    await communicator.receive_json_from()

    await communicator.send_json_to({
        'method': 'D',
        'values': {
            'message_id': 1,
        },
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })
    # await communicator.receive_json_from()
    assert expected_response == await communicator.receive_json_from()

    assert start_messages_count - 1 == await async_count_db(Message)
    assert start_messages_count_room - 1 == await async_count_filter_db(
        Message,
        room_id=1,
    )

    # Close
    await communicator.disconnect()
