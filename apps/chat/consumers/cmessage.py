"""
...
"""

import json
from typing import Any, Dict, Union

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.chat.consumers.utils import get_room_or_error
from apps.chat.models import Message, Room
from apps.chat.serializers import MessageHeavySerializer, RequestMessageSerializer
from apps.user.decorators import token_required, user_active

# from django.utils import timezone
# from django.contrib.auth.models import AnonymousUser, User


class MessageConsumer(AsyncWebsocketConsumer):
    """
    ...
    """

    async def connect(self):
        """
        Store which rooms the user has joined on this connection
        """
        self.rooms = set()
        await self.accept()

    async def disconnect(self, close_code):
        """
        Leave all the rooms we are still in
        """
        for room_id in list(self.rooms):
            try:
                await self.leave_room(room_id)
            except Exception:
                pass

    @token_required
    async def receive(self, text_data: str):
        """
        Receive message from WebSocket
        """
        request: Dict[str, Any] = self.validate_request(text_data)
        if "errors" in request:
            await self.send(text_data=json.dumps(request))
        else:
            # print(request)
            if request["method"] == "C":
                response = await self.create_message(request["values"])
                # print(response)
                if "errors" in response:
                    # print(response)
                    await self.send(text_data=json.dumps(response))
                else:
                    await self.channel_layer.group_send(
                        str(response["room_id"]),
                        {
                            "type": "message_event",
                            "method": request["method"],
                            "data": response,
                        },
                    )
            elif request["method"] == "D":
                response = await self.delete_message(request["values"])
                print(response)
                if "errors" in response:
                    await self.send(text_data=json.dumps(response))
                else:
                    await self.channel_layer.group_send(
                        str(response["room_id"]),
                        {
                            "type": "message_event",
                            "method": request["method"],
                            "data": response,
                        },
                    )
            elif request["method"] == "J":
                await self.join_room(request["values"]["room_id"])
            elif request["method"] == "E":
                await self.leave_room(request["values"]["room_id"])
            else:
                response = await self.list_messages_room(
                    room_id=request["values"]["room_id"]
                )
                if "errors" in response:
                    await self.send(text_data=json.dumps(response))
                else:
                    await self.send(
                        text_data=json.dumps(
                            {"method": request["method"], "data": response,}
                        )
                    )

    @user_active
    async def message_event(self, event: Dict[str, Any]):
        """
        Receive message from room group
        """
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"method": event["method"], "data": event["data"],})
        )

    @user_active
    async def join_room(self, room_id: int):
        """
        ...
        """
        room: Union[Any, Dict[str, Any]] = await get_room_or_error(room_id)
        if isinstance(room, dict):
            # print(room)
            await self.send(text_data=json.dumps(room))
        else:
            # Store that we're in the room
            self.rooms.add(room_id)
            # Add them to the group so they get room messages
            await self.channel_layer.group_add(
                str(room_id), self.channel_name,
            )
            # Instruct their client to finish opening the room
            await self.send(text_data=json.dumps({"join": room.id, "name": room.name,}))
            # notify users
            await self.channel_layer.group_send(
                str(room_id),
                {
                    "type": "chat_join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                    "method": "J",
                },
            )

    @user_active
    async def leave_room(self, room_id: int):
        """
        ...
        """
        room = await get_room_or_error(room_id)
        if isinstance(room, dict):
            # print(room)
            await self.send(text_data=json.dumps(room))
        else:
            # Remove that we're in the room
            self.rooms.discard(room_id)
            # Remove them from the group so they no longer get room messages
            await self.channel_layer.group_discard(
                str(room_id), self.channel_name,
            )
            # Instruct their client to finish closing the room
            await self.send(text_data=json.dumps({"leave": room.id,}))
            # notify users
            await self.channel_layer.group_send(
                str(room_id),
                {
                    "type": "chat_join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                    "method": "E",
                },
            )

    async def chat_join(self, event: Dict[str, Any]):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send(
            text_data=json.dumps(
                {
                    "method": event["method"],
                    "data": {"room": event["room_id"], "username": event["username"]},
                },
            )
        )

    @database_sync_to_async
    def list_messages_room(self, room_id: int) -> Union[Dict[str, str], Any]:
        """
        listar room
        """
        try:
            # verify that there is a room
            Room.objects.get(id=room_id)
            messages = MessageHeavySerializer(
                Message.objects.filter(room_id=room_id).order_by("id"), many=True,
            ).data
            return messages
        except Exception as e:
            return {"errors": {"exception": str(e)}}

    @database_sync_to_async
    def create_message(self, values: Dict[str, Any]):
        """
        Crear message o retornar error
        """
        try:
            message = Message.objects.create(
                text=values["text"], room_id=values["room_id"],
            )
            serializer = MessageHeavySerializer(message)
            return serializer.data
        except Exception as e:
            return {"errors": {"exception": str(e)}}

    @database_sync_to_async
    def delete_message(self, values: Dict[str, Any]):
        """
        eliminar message o retornar error
        """
        try:
            message = Message.objects.get(pk=values["message_id"],)
            message_id: int = message.id
            data = MessageHeavySerializer(message).data
            message.delete()
            data["id"] = message_id
            return data
        except Exception as e:
            return {"errors": {"exception": str(e)}}

    def validate_request(self, text_data: str) -> Dict[str, Any]:
        """
        validar contenido solicitud
        """
        # try:

        text_data_json: Dict["str", Any] = json.loads(text_data)
        # print(text_data_json)
        serializer = RequestMessageSerializer(data=text_data_json)
        if serializer.is_valid():
            return serializer.data

        return {"errors": serializer.errors}

        # except Exception as e:
        #     return {'errors': str(e)}
