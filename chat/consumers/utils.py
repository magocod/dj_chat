"""
Buscar room
"""

# standard library
from typing import Any, Awaitable, Dict, Union

# third-party
from channels.db import database_sync_to_async

# Django
from django.contrib.auth.models import User

# local Django
from chat.models import Room

result = Union[Dict[str, Any], Room]

@database_sync_to_async
def get_room_or_error(room_id: int, user: User) -> Awaitable[result]:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if user == None:
        return {'errors': 'user_no_exist'}

    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        return {'errors': 'room_no_exist'}

    # Check permissions
    # ...

    return room
