"""
...
"""

# Django
from django.utils import timezone
# third-party
from rest_framework import serializers

# local Django
from chat.models import Room


class RequestSerializer(serializers.Serializer):
    """
    ...
    """
    OPERATIONS = (
        ('U', 'UPSERT'),
        ('D', 'DELETE'),
        ('L', 'LIST'),
    )
    method = serializers.ChoiceField(choices=OPERATIONS)
    token = serializers.CharField(max_length=40)
    values = serializers.JSONField()


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
