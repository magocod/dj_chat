"""
...
"""

# standard library
import json
from typing import Any, Dict, List, Union

# third-party
# from channels.auth import get_user, login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# Django
from django.utils import timezone

# local Django
from chat.models import Room
from chat.serializers import RequestSerializer, RoomHeavySerializer
from user.decorators import token_required, user_active

# from django.contrib.auth.models import AnonymousUser, User


List_or_Dict = Union[Dict[str, str], List[Dict[str, Any]]]


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
                response: Dict[str, Any] = await self.upsert_room(
                    request['values']
                )
                # print(response)
                if 'errors' in response:
                    await self.send(
                        text_data=json.dumps(response)
                    )
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
                response: Dict[str, Any] = await self.delete_room(
                    request['values']
                )
                if 'errors' in response:
                    await self.send(text_data=json.dumps(response))
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'room_event',
                            'method': request['method'],
                            'data': response,
                        }
                    )
            else:
                response: List_or_Dict = await self.list_room()
                if isinstance(response, dict):
                    await self.send(text_data=json.dumps(response))
                else:
                    await self.send(text_data=json.dumps({
                        'method': request['method'],
                        'data': response,
                    }))

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
    def list_room(self) -> List_or_Dict:
        """
        listar room
        """
        try:
            serializer = RoomHeavySerializer(
                Room.objects.all().order_by('id'),
                many=True,
            )
            return serializer.data
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
            serializer = RoomHeavySerializer(room)
            return serializer.data
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    @database_sync_to_async
    def delete_room(self, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        eliminar room o retornar error
        """
        try:
            # retorna (numero eliminados, dict tipos eliminados)
            count, _ = Room.objects.filter(
                pk__in=values['pk_list'],
            ).delete()
            return {
                'count': count,
                'pk_list': values['pk_list'],
            }
        except Exception as e:
            return {'errors': {'exception': str(e)}}

    def validate_request(self, text_data: str) -> Dict[str, Any]:
        """
        validar contenido solicitud
        """
        try:
            text_data_json: Dict['str', Any] = json.loads(text_data)
            # print(text_data_json)
            serializer = RequestSerializer(data=text_data_json)
            if serializer.is_valid():
                return serializer.data

            return serializer.errors
        except Exception as e:
            return {'errors': str(e)}
