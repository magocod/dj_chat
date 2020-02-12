"""
Modelos
"""

# local Django
from django.db import models
from django.utils import timezone


class Room(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=50, unique=True)
    updated = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """
    ...
    """

    text = models.TextField()
    updated = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE,)
