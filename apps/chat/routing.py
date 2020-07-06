"""
...
"""


from django.urls import path

from apps.chat.consumers.cmessage import MessageConsumer
from apps.chat.consumers.croom import RoomConsumer

websocket_urlpatterns = [
    path("ws/chat/", MessageConsumer),
    path("ws/rooms/", RoomConsumer),
]
