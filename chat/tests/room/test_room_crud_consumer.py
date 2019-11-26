"""
...
"""

# standard library

# third-party
import pytest

# Django
# from channels.testing import HttpCommunicator
from channels.testing import WebsocketCommunicator

# local Django
from chat.models import Room
from chat.consumers.croom import RoomConsumer

from tests.db import count_db

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.rooms_consumers]


@pytest.mark.asyncio
@pytest.mark.rooms_crud
async def test_room_create():
    """
    ...
    """
    count: int = await count_db(Room)

    assert count == 0
