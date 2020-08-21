"""
...
"""

# import asyncio

import pytest
from channels.testing import WebsocketCommunicator

# from tests.comunicators import (
#     TOKENS,
#     generate_ws_comunicators,
# )
from apps.chat.consumers.cmessage import MessageConsumer

pytestmark = [pytest.mark.django_db, pytest.mark.messages_consumers]


@pytest.mark.asyncio
@pytest.mark.chats_rooms
async def test_consumer_join_room(auth_token):
    """
    ...
    """
    communicator_1 = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_1.connect()
    assert connected

    # Test sending json
    await communicator_1.send_json_to(
        {
            "method": "J",
            "values": {"room_id": 1},
            "token": auth_token["super_user_admin"],
        }
    )

    response_user = await communicator_1.receive_json_from()
    assert response_user == {"join": 1, "name": "name_0"}

    response_group = await communicator_1.receive_json_from()
    assert response_group == {
        "method": "J",
        "data": {
            "room": 1,
            "username": "super_user_admin",
        },  # nombre usuario del token
    }

    # Close
    await communicator_1.disconnect()


@pytest.mark.asyncio
@pytest.mark.chats_rooms
async def test_consumer_leave_room(auth_token):
    """
    ...
    """
    communicator_1 = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_1.connect()
    assert connected

    # Test sending json
    await communicator_1.send_json_to(
        {
            "method": "E",
            "values": {"room_id": 1},
            "token": auth_token["super_user_admin"],
        }
    )
    response_user = await communicator_1.receive_json_from()
    assert response_user == {"leave": 1}

    # Close
    await communicator_1.disconnect()


@pytest.mark.asyncio
@pytest.mark.chats_rooms
async def test_notify_users_of_new_members_entering_the_room(auth_token):
    """
    ...
    """
    # Get the current event loop.
    # loop = asyncio.get_running_loop()
    # fut = loop.create_future()

    # await generate_ws_comunicators(
    #     fut,
    #     TOKENS,
    #     1,
    #     MessageConsumer,
    #     '/ws/chat/',
    # )
    # await fut
    # communicator_in_room, communicator_entering, *others = fut.result()

    communicator_in_room = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_in_room.connect()
    assert connected

    communicator_entering = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_entering.connect()
    assert connected

    await communicator_in_room.send_json_to(
        {
            "method": "J",
            "values": {"room_id": 1},
            "token": auth_token["super_user_admin"],
        }
    )
    # notify user
    await communicator_in_room.receive_json_from()
    # notify user group
    await communicator_in_room.receive_json_from()

    await communicator_entering.send_json_to(
        {"method": "J", "values": {"room_id": 1}, "token": auth_token["user_staff"],}
    )
    # notify user
    await communicator_entering.receive_json_from()
    # notify user group
    await communicator_entering.receive_json_from()

    response = await communicator_in_room.receive_json_from()
    assert response == {
        "method": "J",
        "data": {
            "room": 1,
            "username": "super_user_admin",
        },  # nombre usuario del token
    }

    # Close
    await communicator_in_room.disconnect()
    await communicator_entering.disconnect()


@pytest.mark.asyncio
@pytest.mark.chats_rooms
async def test_notify_users_of_the_departure_of_another_user_from_the_room(auth_token):
    """
    ...
    """
    communicator_in_room = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_in_room.connect()
    assert connected

    communicator_coming_out = WebsocketCommunicator(MessageConsumer, "/ws/chat/",)
    connected, _ = await communicator_coming_out.connect()
    assert connected

    await communicator_in_room.send_json_to(
        {
            "method": "J",
            "values": {"room_id": 1},
            "token": auth_token["super_user_admin"],
        }
    )
    # notify user
    await communicator_in_room.receive_json_from()
    # notify user group
    await communicator_in_room.receive_json_from()

    await communicator_coming_out.send_json_to(
        {"method": "J", "values": {"room_id": 1}, "token": auth_token["user_staff"],}
    )
    # notify user
    await communicator_coming_out.receive_json_from()
    # notify user group
    await communicator_coming_out.receive_json_from()
    # join communicator_coming_out
    await communicator_in_room.receive_json_from()

    await communicator_coming_out.send_json_to(
        {"method": "E", "values": {"room_id": 1}, "token": auth_token["user_staff"],}
    )
    # notify user
    await communicator_coming_out.receive_json_from()

    response = await communicator_in_room.receive_json_from()
    assert response == {
        "method": "E",
        "data": {
            "room": 1,
            "username": "super_user_admin",
        },  # nombre usuario del token
    }

    # Close
    await communicator_in_room.disconnect()
    await communicator_coming_out.disconnect()


@pytest.mark.asyncio
@pytest.mark.chats_rooms
async def test_notify_users_of_users_disconnected_by_force(auth_token):
    """
    ...
    """
    communicator_in_room = WebsocketCommunicator(MessageConsumer, "/ws/chat/")
    connected, _ = await communicator_in_room.connect()
    assert connected

    communicator_force_exit = WebsocketCommunicator(MessageConsumer, "/ws/chat/",)
    connected, _ = await communicator_force_exit.connect()
    assert connected

    await communicator_in_room.send_json_to(
        {
            "method": "J",
            "values": {"room_id": 1},
            "token": auth_token["super_user_admin"],
        }
    )
    # notify user
    await communicator_in_room.receive_json_from()
    # notify user group
    await communicator_in_room.receive_json_from()

    await communicator_force_exit.send_json_to(
        {"method": "J", "values": {"room_id": 1}, "token": auth_token["user_staff"],}
    )
    # notify user
    await communicator_force_exit.receive_json_from()
    # notify user group
    await communicator_force_exit.receive_json_from()
    # join comunicator_force_exit
    await communicator_in_room.receive_json_from()
    # force exit
    await communicator_force_exit.disconnect()

    # user exit
    response = await communicator_in_room.receive_json_from()
    assert response == {
        "method": "E",
        "data": {
            "room": 1,
            "username": "super_user_admin",
        },  # nombre usuario del token
    }

    # Close
    await communicator_in_room.disconnect()
