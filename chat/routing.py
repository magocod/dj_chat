"""
...
"""

# Django
from django.urls import path

# local Django
from chat.consumers.cmessage import MessageConsumer
from chat.consumers.croom import RoomConsumer

websocket_urlpatterns = [
	path('ws/chat/', MessageConsumer),
  	path('ws/rooms/', RoomConsumer),
]