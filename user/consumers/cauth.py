"""
...
"""

# third-party
from channels.generic.websocket import AsyncWebsocketConsumer


class AuthConsumer(AsyncWebsocketConsumer):
    """
    ...
    """
    room_group_name: str = 'users'

    async def connect(self):
        """
        Join room group
        """
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # print(self.scope["headers"])
        await self.accept()

    async def disconnect(self, close_code):
        """
        Leave room group
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data: str):
        """
        Receive message from WebSocket
        """
        await self.send(text_data=text_data)
