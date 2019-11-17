"""
...
"""

# standard library
import asyncio

# third-party
import pytest

# Django
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer

# local Django
from apps.notification.consumers import NotifyConsumer

# permitir acceso a db
pytestmark = pytest.mark.django_db

@pytest.mark.asyncio
@pytest.mark.notifications_consumers
async def test_notify_authenticated_group_clients():
    """
    verificar recepcion de notificacion consumidor autenticado
    """

    communicator = WebsocketCommunicator(NotifyConsumer, "/ws/notifications/")
    connected1, subprotocol1 = await communicator.connect()
    assert connected1

    # communicator2 = WebsocketCommunicator(NotifyConsumer, "/ws/notifications/")
    # connected2, subprotocol2 = await communicator.connect()
    # assert connected2

    # # Test sending text
    request_admin = {'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6d30'}
    # request_user = {'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120'}

    # autenticar
    await communicator.send_json_to(request_admin)
    response1 = await communicator.receive_json_from()
    assert response1 == request_admin

    # await communicator2.send_json_to(request_user)
    # response2 = await communicator2.receive_json_from()
    # assert response2 == request_user

    # notificar a los consumidores
    channel_layer = get_channel_layer()
    message = {
        'type': 'notify_event',
        'payload': 1,
        'details': {'test': 'data'},
    }
    await channel_layer.group_send('notifications', message)

    # (comprobar si existe evento)
    assert await communicator.receive_nothing(timeout=0.1) == False
    # assert await communicator2.receive_nothing(timeout=0.1) == False

    # consumidores recibir notificacion
    notification1 = await communicator.receive_json_from()
    del message['type']
    assert notification1 == message
    # notification2 = await communicator2.receive_json_from()
    # assert notification2 == message

    # (comprobar si existe evento)
    assert await communicator.receive_nothing(timeout=0.1) == True
    # assert await communicator2.receive_nothing(timeout=0.1) == True

    # Close
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.notifications_consumers
async def test_notify_no_authenticated_client():
    """
    verificar que no se envien notificacion consumidores no autenticados
    """

    communicator = WebsocketCommunicator(NotifyConsumer, "/ws/notifications/")
    connected, subprotocol = await communicator.connect()
    assert connected

    # notificar a los consumidores
    channel_layer = get_channel_layer()
    message = {
        'type': 'notify_event',
        'payload': 1,
        'details': {'test': 'data'},
    }
    await channel_layer.group_send('notifications', message)

    # consumidores recibir notificacion (comprobar si existe evento)
    assert await communicator.receive_nothing(timeout=1) == True
    # assert response == None

    # Close
    await communicator.disconnect()
