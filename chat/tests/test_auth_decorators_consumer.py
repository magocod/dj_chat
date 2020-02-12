"""
...
"""

# third-party
import pytest
from channels.testing import WebsocketCommunicator

# local Django
from chat.consumers.croom import RoomConsumer

# permitir acceso a db
pytestmark = pytest.mark.django_db


@pytest.mark.asyncio
@pytest.mark.auth_decorator
async def test_consumer_valid_token():
    """
    Conexion de cliente con token de autenticacion valida
    """

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, subprotocol = await communicator.connect()
    assert connected
    # Test sending text
    request = {"token": "20fd382ed9407b31e1d5f928b5574bb4bffe6120"}
    # await communicator.send_to(text_data='')
    await communicator.send_json_to(request)
    # response = await communicator.receive_from()
    # response = await communicator.receive_json_from()
    # assert response == request
    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.auth_decorator
async def test_consumer_no_token():
    """
    Conexion de cliente sin proveer token de autenticacion
    """

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, subprotocol = await communicator.connect()
    assert connected
    # Test sending text
    request = {"no_token": "123"}
    await communicator.send_json_to(request)
    response = await communicator.receive_json_from()
    assert response == {
        "code": 401,
        "details": "Authentication credentials were not provided",
    }
    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.auth_decorator
async def test_consumer_invalid_token():
    """
    Conexion de cliente sin proveer token de autenticacion
    """

    communicator = WebsocketCommunicator(RoomConsumer, "/ws/rooms/")
    connected, subprotocol = await communicator.connect()
    assert connected
    # Test sending text
    request = {"token": "123"}
    await communicator.send_json_to(request)
    response = await communicator.receive_json_from()
    assert response == {"code": 401, "details": "user or token no exist"}
    # Close
    await communicator.disconnect()
