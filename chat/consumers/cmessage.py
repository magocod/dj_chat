"""
...
"""

# standard library
import json
from typing import Any, Dict, List, Tuple, Union

# third-party
# from channels.auth import get_user, login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# Django
from django.utils import timezone
# from django.contrib.auth.models import AnonymousUser, User

# local Django
from chat.models import Message, Room
from chat.consumers.utils import get_room_or_error
from user.decorators import user_active, token_required

class MessageConsumer(AsyncWebsocketConsumer):
    """
    ...
    """
    error_event: str = 'error_message'
    valid_operations: Tuple[str] = ('c', 'r', 'd', 'j', 'l')
    valid_properties: Tuple[str] = ('method', 'values', 'token')

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
            except:
                pass

    @token_required
    async def receive(self, text_data: str):
        """
        Receive message from WebSocket
        """
        request: Dict[str, Any] = self.validate_request(text_data)
        if 'errors' in request:
            await self.send(text_data=json.dumps(request))
        else:
            if request['method'] == 'c':
                message: Union[Dict[str, str], Room] = await self.create_message(request['values'])
                # print(message)
                if isinstance(message, dict):
                    # print(request)
                    await self.send(text_data=json.dumps(message))
                else:
                    await self.channel_layer.group_send(
                        str(request['values']['room_id']),
                        {
                            'type': 'message_event',
                            'method': request['method'],
                            'id': message.id,
                            'text': message.text,
                            'updated': str(message.updated),
                            'timestamp': str(message.timestamp),
                            'room_id': message.room_id,
                        }
                    )
            elif request['method'] == 'd':
                result: Union[Dict[str, str], bool] = await self.delete_message(
                    request['values']
                )
                if isinstance(result, dict):
                    # print(result)
                    await self.send(text_data=json.dumps(result))
                else:
                    await self.channel_layer.group_send(
                        str(request['values']['room_id']),
                        {
                            'type': 'message_delete',
                            'method': request['method'],
                            'details': request['values']['message_id'],
                        }
                    )
            elif request['method'] == 'j':
                await self.join_room(request['values']['room_id'])
            elif request['method'] == 'l':
                await self.leave_room(request['values']['room_id'])
            else:
                messages: List[Tuple[Any]] = await self.list_messages_room(
                    room_id=request['values']['room_id']
                )
                if isinstance(messages, dict):
                    # print(result)
                    await self.send(text_data=json.dumps(messages))
                else:
                    await self.send(text_data=json.dumps({
                        'method': request['method'],
                        'data': messages,
                    }))
                    await self.send(text_data=json.dumps({
                        'method': request['method'],
                        'rooms': tuple(self.rooms),
                    }))

    @user_active
    async def message_list(self, event: Dict[str, Any]):
        """
        get list message room
        """

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'data': event['list'],
        }))

    @user_active
    async def message_event(self, event: Dict[str, Any]):
        """
        Receive message from room group
        """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'id' : event['id'],
            'text': event['text'],
            'updated': event['updated'],
            'timestamp': event['timestamp'],
            'room_id': event['room_id'],
        }))

    @user_active
    async def message_delete(self, event: Dict[str, Any]):
        """
        deleted message
        """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'details' : event['details'],
        }))

    @user_active
    async def join_room(self, room_id: int):
        """
        ...
        """
        room: Union[Room, Dict[str, Any]] = await get_room_or_error(room_id)
        if isinstance(room, dict):
            # print(room)
            await self.send(text_data=json.dumps(room))
        else:
            # notify users
            await self.channel_layer.group_send(
                str(room_id),
                {
                    'type': 'chat_join',
                    'room_id': room_id,
                    'username': self.scope['user'].username,
                }
            )
            # Store that we're in the room
            self.rooms.add(room_id)
            # Add them to the group so they get room messages
            await self.channel_layer.group_add(
                str(room_id),
                self.channel_name,
            )
            # Instruct their client to finish opening the room
            await self.send(
                text_data=json.dumps(
                    {
                        'join': str(room.id),
                        'name': room.name,
                    }
                )
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
            # notify users
            await self.channel_layer.group_send(
                str(room_id),
                {
                    'type': 'chat_leave',
                    'room_id': room_id,
                    'username': self.scope['user'].username,
                }
            )
        # Remove that we're in the room
        self.rooms.discard(room_id)
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            str(room_id),
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send(
            text_data=json.dumps(
                {
                    'leave': str(room.id),
                }
            )
        )

    async def chat_join(self, event: Dict[str, Any]):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send(
            text_data=json.dumps(
                {
                    'msg_type': 'j',
                    'room': event['room_id'],
                    'username': event['username'],
                },
            )
        )

    async def chat_leave(self, event: Dict[str, Any]):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send(
            text_data=json.dumps(
                {
                    'msg_type': 'l',
                    'room': event['room_id'],
                    'username': event['username'],
                },
            )
        )

    async def error_message(self, event: Dict[str, Any]):
        """
        Notificar error
        nota: requerido para decorador token_required
        """
        # print(event['type'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'code': event['code'],
            'details': event['details'],
        }))

    @database_sync_to_async
    def list_messages_room(self, room_id: int) -> Union[Dict[str, str], Room]:
        """
        listar room
        """
        try:
            return tuple(
                Message.objects.filter(room_id=room_id).order_by('id').values(
                    'id',
                    'text',
                    'room_id',
                )
            )
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    @database_sync_to_async
    def create_message(self, values: Dict[str, Any]) -> Union[Dict[str, str], Message]:
        """
        Crear message o retornar error
        """
        try:
            return Message.objects.create(
                text=values['text'],
                room_id=values['room_id']
            )
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    @database_sync_to_async
    def delete_message(self, values: Dict[str, Any]) -> bool:
        """
        eliminar message o retornar error
        """
        try:
            Message.objects.filter(
                pk=values['message_id'],
            ).delete()
            return True
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    def validate_request(self, text_data: str) -> Dict[str, Any]:
        """
        validar contenido solicitud
        """
        try:
            text_data_json: Dict[str, Any] = json.loads(text_data)
            # print(text_data_json)
            # validar propiedades
            if tuple(text_data_json.keys()) == self.valid_properties:
                if text_data_json['method'] in self.valid_operations:
                    return text_data_json
                else:
                    return {'errors': {'invalid_method': text_data_json['method']}}
            else:
                return {
                    'errors': {'invalid_content': text_data_json},
                    'required': self.valid_properties,
                }
        except Exception as e:
            return {'errors': {'invalid_json': str(e)}}
