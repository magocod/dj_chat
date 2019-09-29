"""
...
"""

# standard library
import asyncio
import functools
import json
from typing import Any, Dict, List, Tuple, Union

# third-party
from channels.auth import get_user, login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token

# Django
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser, User

# local Django
from chat.models import Room


@database_sync_to_async
def user_token(token_key: str):
  try:
    tk = Token.objects.get(key= token_key)
    return User.objects.get(id= tk.user_id)
  except Token.DoesNotExist:
    return False
  except User.DoesNotExist:
    return False

def user_active(func):
    """
    Verificar existencia de usuario
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # optener atributo cls
        scope = getattr(self, 'scope', {'user': {'id': None}})
        # print(func)
        print('dec id: ', scope['user'].id)
        # print(scope['user'])
        if scope['user'].id != None:
            return func(self, *args, **kwargs)
        else:
            return asyncio.sleep(1)
    return wrapper

class RoomConsumer(AsyncWebsocketConsumer):
    """
    ...
    """
    room_group_name: str = 'rooms'
    valid_operations: Tuple[str] = ('c', 'r', 'u', 'd')
    valid_properties: Tuple[str] = ('method', 'values')

    async def connect(self):
        """
        Join room group
        """
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.scope["user"])
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
        print(self.scope["user"].id)
        print(type(self.scope["user"]))
        if self.scope["user"].id == None:
            print('usuario asignar')
            # login the user to this session.
            user = await user_token('2e4157c9706829e91505b63cc4bdba3ee8702604')
            self.scope['user'] = user
            # await login(self.scope, user)
        else:
            print('usuario asignado')

        request: Dict[str, Any] = self.validate_request(text_data)
        # print(request)
        if 'errors' in request:
            await self.send(text_data=json.dumps(request))
        else:
            if request['method'] == 'c' or request['method'] == 'u':
                room: Union[Dict[str, str], Room] = await self.update_room(request['values'])
                # print(room)
                if isinstance(room, dict):
                    # print(request)
                    await self.send(text_data=json.dumps(room))
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'room_event',
                            'method': request['method'],
                            'id': room.id,
                            'name': room.name,
                            'updated': str(room.updated),
                            'timestamp': str(room.timestamp),
                        }
                    )
            elif request['method'] == 'd':
                result: Union[Dict[str, str], Tuple[Any]] = await self.delete_room(
                    request['values']
                )
                if isinstance(result, dict):
                    # print(result)
                    await self.send(text_data=json.dumps(result))
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'room_remove',
                            'method': request['method'],
                            'details': result,
                        }
                    )
            else:
                rooms: List[Tuple[Any]] = await self.list_room()
                if isinstance(rooms, dict):
                    # print(result)
                    await self.send(text_data=json.dumps(rooms))
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'room_list',
                            'method': 'r',
                            'list': rooms,
                        }
                    )

    @user_active
    async def room_list(self, event: Dict[str, Any]):
        """
        Receive message from room group
        """
        # print(event['type'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'data': event['list'],
        }))

    @user_active
    async def room_event(self, event: Dict[str, Any]):
        """
        Receive message from room group
        """
        # print(event['type'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'id' : event['id'],
            'name': event['name'],
            'updated': event['updated'],
            'timestamp': event['timestamp'], 
        }))

    async def room_remove(self, event: Dict[str, Any]):
        """
        Receive message from room group
        """
        # print(event['type'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'details': event['details'],
        }))

    @database_sync_to_async
    def list_room(self) -> Union[Dict[str, str], Room]:
        """
        listar room
        """
        try:
            return tuple(Room.objects.all().order_by('id').values('id', 'name'))
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    @database_sync_to_async
    def update_room(self, values: Dict[str, Any]) -> Union[Dict[str, str], Room]:
        """
        Crear room o retornar error
        """
        try:
            room, created = Room.objects.update_or_create(
                name=values['name'],
                # defaults={'updated': timezone.now()},
            )
            return room
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    @database_sync_to_async
    def delete_room(self, values: Dict[str, Any]) -> Tuple[Any]:
        """
        eliminar room o retornar error
        retorna (numoro eliminados, dict tipos eliminados)
        """
        try:
            return Room.objects.filter(
                pk__in= values['pk_list'],
            ).delete()
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    def validate_request(self, text_data: str) -> Dict[str, Any]:
        """
        validar contenido solicitud
        """
        try:
            text_data_json: Dict['str', Any] = json.loads(text_data)
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
