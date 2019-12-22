"""
ejecutar comando creacion de usuarios por defecto
"""

# Django
from django.core.management.base import BaseCommand

# local Django
from chat.models import Message, Room


class Command(BaseCommand):
    """
    ...
    """
    def handle(self, *args, **options):
        """
        ...
        """
        # rooms
        rooms_instances = [
            Room(name=f'name_{number}')
            for number in range(4)
        ]
        Room.objects.bulk_create(rooms_instances)
        # messages
        messages_room_1_instances = [
            Message(
                text=f'text{number}',
                room_id=1,
            )
            for number in range(4)
        ]
        messages_room_2_instances = [
            Message(
                text=f'text{number}',
                room_id=2,
            )
            for number in range(3)
        ]
        Message.objects.bulk_create(messages_room_1_instances)
        Message.objects.bulk_create(messages_room_2_instances)
