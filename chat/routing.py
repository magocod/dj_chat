"""
...
"""

# Django
from django.urls import path

# local Django
from chat.consumers.croom import RoomConsumer

websocket_urlpatterns = [
  	path('ws/rooms/', RoomConsumer),
]