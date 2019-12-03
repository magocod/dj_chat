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
from chat.models import Room
from chat.serializers import RequestSerializer, RoomSerializer, RoomHeavySerializer

from user.decorators import user_active, token_required

class RoomConsumer(AsyncWebsocketConsumer):
    """
    ...
    """
    room_group_name: str = 'rooms'

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

    @token_required
    async def receive(self, text_data: str):
        """
        Receive message from WebSocket
        """
        request: Dict[str, Any] = self.validate_request(text_data)
        # print(request)
        if 'errors' in request:
            await self.send(text_data=json.dumps(request))
        else:
            if request['method'] == 'U':
                response = await self.upsert_room(request['values'])
                # print(response)
                if 'errors' in response:
                    await self.send(text_data=json.dumps(response))
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'room_event',
                            'method': request['method'],
                            'data': None,
                        }
                    )
            elif request['method'] == 'D':
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
                            'type': 'room_event',
                            'method': request['method'],
                            'data': result,
                        }
                    )
            else:
                rooms: List[Tuple[Any]] = await self.list_room()
                if isinstance(rooms, dict):
                    # print(result)
                    await self.send(text_data=json.dumps(rooms))
                else:
                    await self.send(text_data=json.dumps({
                        'method': request['method'],
                        'data': rooms,
                    }))
                    # await self.channel_layer.group_send(
                    #     self.room_group_name,
                    #     {
                    #         'type': 'room_list',
                    #         'method': 'r',
                    #         'list': rooms,
                    #     }
                    # )

    @user_active
    async def room_list(self, event: Dict[str, Any]):
        """
        Receive message from room group
        """
        # print(event['type'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'data': event['data'],
        }))

    @user_active
    async def room_event(self, event: Dict[str, Any]):
        """
        Receive message from room group
        """
        print(event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method': event['method'],
            'data': event['data'],
        }))

    @database_sync_to_async
    def list_room(self) -> Union[Dict[str, str], Tuple[Any]]:
        """
        listar room
        """
        try:
            return tuple(Room.objects.all().order_by('id').values('id', 'name'))
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    @database_sync_to_async
    def upsert_room(self, values: Dict[str, Any]) -> Dict[str, str]:
        """
        Crear o actualizar room, 
        retornar exception
        """
        try:
            room, _ = Room.objects.update_or_create(
                name=values['name'],
                defaults={'updated': timezone.now()},
            )
            # print(room.id)
            serializer = RoomHeavySerializer(room)
            return serializer.data
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
                pk__in=values['pk_list'],
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
            serializer = RequestSerializer(data=text_data_json)
            if serializer.is_valid():
                return serializer.data

            return serializer.errors
            
        except Exception as e:
            return {'errors': str(e) }
