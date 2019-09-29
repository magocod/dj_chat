"""
Buscar room
"""

# standard library
from typing import Any, Awaitable, Dict, Union

# third-party
from channels.db import database_sync_to_async

# local Django
from chat.models import Room

result = Union[Dict[str, Any], Room]

@database_sync_to_async
def get_room_or_error(room_id: int) -> Awaitable[result]:
    """
    check permissions.
    """
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        return {'errors': 'room_no_exist'}

    return room
