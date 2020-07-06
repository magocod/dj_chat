"""
...
"""

# local Django
from chat.consumers.cmessage import MessageConsumer
from chat.consumers.croom import RoomConsumer
# Django
from django.urls import path

websocket_urlpatterns = [
    path("ws/chat/", MessageConsumer),
    path("ws/rooms/", RoomConsumer),
]
