"""
Señales eventos base de datos
"""

# third-party
import channels.layers
from asgiref.sync import async_to_sync

# Django
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# local Django
from chat.models import Room, Message

@receiver(post_save, sender=Room)
def RoomUpdated(sender, instance, **kwargs):
    """
    ...
    """
    group_name: str = 'rooms'
    channel_layer = channels.layers.get_channel_layer()
    # print(instance)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'room_event',
            'method': 'u',
            'id': instance.id,
            'name': instance.name,
            'updated': str(instance.updated),
            'timestamp': str(instance.timestamp),
        }
    )

@receiver(post_delete, sender=Room)
def RoomDeleted(sender, instance, **kwargs):
    """
    ...
    """
    group_name: str = 'rooms'
    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'room_event',
            'method': 'd',
            'id': instance.id,
            'name': instance.name,
            'updated': str(instance.updated),
            'timestamp': str(instance.timestamp),
        }
    )
