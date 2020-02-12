"""
...
"""

# third-party
import pytest
from channels.testing import WebsocketCommunicator

# Django
from chat.consumers.cmessage import MessageConsumer

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.messages_consumers]


@pytest.mark.asyncio
@pytest.mark.chats_exists
async def test_join_a_room_that_does_not_exist():
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {
            "method": "J",
            "values": {"room_id": 100},
            "token": "20fd382ed9407b31e1d5f928b5574bb4bffe6120",
        }
    )

    response = await communicator.receive_json_from()
    assert response == {"errors": f"room_do_es_not_exist: {100}"}

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.chats_exists
async def test_leave_a_room_that_does_not_exist():
    """
    ...
    """
    communicator = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    # Test sending json
    await communicator.send_json_to(
        {
            "method": "E",
            "values": {"room_id": 100},
            "token": "20fd382ed9407b31e1d5f928b5574bb4bffe6120",
        }
    )

    response = await communicator.receive_json_from()
    assert response == {"errors": f"room_do_es_not_exist: {100}"}

    # Close
    await communicator.disconnect()
