"""
...
"""

# Django
from django.utils import timezone
# third-party
from rest_framework import serializers

# local Django
from chat.models import Message, Room


class RequestSerializer(serializers.Serializer):
    """
    ...
    """
    OPERATIONS = (
        ('U', 'UPSERT'),
        ('D', 'DELETE'),
        ('R', 'READ'),
    )
    method = serializers.ChoiceField(choices=OPERATIONS)
    token = serializers.CharField(max_length=40)
    values = serializers.JSONField()


class RequestMessageSerializer(RequestSerializer):
    """
    ...
    """
    OPERATIONS = (
        ('C', 'CREATE'),
        ('D', 'DELETE'),
        ('R', 'READ'),
        ('E', 'EXIT'),
        ('J', 'JOIN'),
    )
    method = serializers.ChoiceField(choices=OPERATIONS)


class RoomSerializer(serializers.Serializer):
    """
    ...
    """
    name = serializers.CharField(max_length=50)
    updated = serializers.DateTimeField(default=timezone.now)
    timestamp = serializers.DateTimeField(default=timezone.now)


class RoomHeavySerializer(serializers.ModelSerializer):
    """
    ...
    """
    id = serializers.IntegerField(read_only=True)

    class Meta:
        """
        ...
        """
        model = Room
        fields = ['id', 'name', 'updated', 'timestamp']


class MessageHeavySerializer(serializers.ModelSerializer):
    """
    ...
    """
    id = serializers.IntegerField(read_only=True)

    class Meta:
        """
        ...
        """
        model = Message
        fields = ['id', 'text', 'room_id', 'updated', 'timestamp']
