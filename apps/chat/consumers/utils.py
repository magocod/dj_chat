"""
Buscar room
"""

from typing import Any, Awaitable, Dict, Union

from channels.db import database_sync_to_async

from apps.chat.models import Room

result = Union[Dict[str, Any], Room]


@database_sync_to_async
def get_room_or_error(room_id: int) -> Awaitable[result]:
    """
    check permissions.
    """
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        return {"errors": f"room_do_es_not_exist: {room_id}"}

    return room
