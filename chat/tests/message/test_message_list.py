"""
...
"""

# third-party
import pytest
from channels.testing import WebsocketCommunicator

# local Django
from chat.consumers.cmessage import MessageConsumer
from chat.models import Message
from chat.serializers import MessageHeavySerializer
from tests.response import create_event_filter_list_message

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.messages_consumers]


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_consumer_messages_room_list():
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, '/ws/chat/')
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to({
        'method': 'R',
        'values': {'room_id': 1},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert response == await create_event_filter_list_message(
        model=Message,
        serializer=MessageHeavySerializer,
        room_id=1,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_consumer_empty_message_room_list():
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, '/ws/chat/')
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to({
        'method': 'R',
        'values': {'room_id': 4},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert response == await create_event_filter_list_message(
        model=Message,
        serializer=MessageHeavySerializer,
        room_id=4,
    )

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_request_room_messages_that_do_not_exist():
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, '/ws/chat/')
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to({
        'method': 'R',
        'values': {'room_id': 100},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    })

    response = await communicator.receive_json_from()
    # assert response == 'y'

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.messages_list
async def test_consumer_message_invalid_operation():
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, '/ws/chat/')
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    request = {
        'method': 'H',
        'values': {'name': ''},
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    }
    await communicator.send_json_to(request)

    response = await communicator.receive_json_from()
    # assert response == 'y'
    assert 'errors' in response

    # Close
    await communicator.disconnect()
