"""
...
"""


from apps.chat.consumers.cmessage import MessageConsumer
from apps.chat.consumers.croom import RoomConsumer

from django.urls import path

websocket_urlpatterns = [
    path("ws/chat/", MessageConsumer),
    path("ws/rooms/", RoomConsumer),
]
