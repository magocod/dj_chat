"""
...
"""


import pytest
from channels.testing import WebsocketCommunicator

from apps.chat.consumers.cmessage import MessageConsumer
from apps.chat.models import Message
from apps.chat.serializers import MessageHeavySerializer

from tests.response import create_event_filter_list_message

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.messages_consumers]


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_consumer_messages_room_list(auth_token):
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {
            "method": "R",
            "values": {"room_id": 1},
            "token": auth_token["super_user_admin"],
        }
    )

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert response == await create_event_filter_list_message(
        model=Message, serializer=MessageHeavySerializer, room_id=1,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_consumer_empty_message_room_list(auth_token):
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {
            "method": "R",
            "values": {"room_id": 4},
            "token": auth_token["super_user_admin"],
        }
    )

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert response == await create_event_filter_list_message(
        model=Message, serializer=MessageHeavySerializer, room_id=4,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_request_room_messages_that_do_not_exist(auth_token):
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {
            "method": "R",
            "values": {"room_id": 100},
            "token": auth_token["super_user_admin"],
        }
    )

    await communicator.receive_json_from()
    # response = await communicator.receive_json_from()
    # assert response == 'y'

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_consumer_message_invalid_operation(auth_token):
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        "method": "H",
        "values": {"name": ""},
        "token": auth_token["super_user_admin"],
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert "errors" in response

    # Close
    await communicator.disconnect()
