"""
Señales eventos base de datos
"""

# third-party
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Django
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# local Django
from chat.models import Room
from chat.serializers import RoomSerializer

@receiver(post_save, sender=Room)
def room_upsert(sender, instance, **kwargs):
    """
    ...
    """
    group_name: str = 'rooms'
    channel_layer = get_channel_layer()
    serializer = RoomSerializer(instance)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'room_event',
            'method': 'U',
            'data': serializer.data,
        }
    )

@receiver(post_delete, sender=Room)
def room_deleted(sender, instance, **kwargs):
    """
    ...
    """
    group_name: str = 'rooms'
    channel_layer = get_channel_layer()
    serializer = RoomSerializer(instance)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'room_event',
            'method': 'D',
            'data': serializer.data,
        }
    )
