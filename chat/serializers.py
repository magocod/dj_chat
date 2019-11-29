"""
...
"""

# Django
from django.utils import timezone

# third-party
from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
    """
    ...
    """
    method = serializers.ChoiceField(choices=('c', 'r', 'u', 'd'))
    token = serializers.CharField(max_length=40)
    values = serializers.JSONField()

class RoomSerializer(serializers.Serializer):
    """
    ...
    """
    name = serializers.CharField(max_length=50)
    updated = serializers.DateTimeField(default=timezone.now)
    timestamp = serializers.DateTimeField(default=timezone.now)
