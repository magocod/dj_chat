"""
Decoradores verificacion de usuarios en consumidores
"""

# standard library
import asyncio
import json
import functools
from typing import Any, Dict, Union

# third-party
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from rest_framework.authtoken.models import Token

# Django
from django.contrib.auth.models import User

@database_sync_to_async
def user_token(token_key: str):
    """
    buscar usuario
    """
    try:
        tk = Token.objects.get(key=token_key)
        return User.objects.get(id=tk.user_id)
    except Token.DoesNotExist:
        return None
    except User.DoesNotExist:
        return None

def user_active(func):
    """
    Verificar existencia de usuario
    """
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        # optener atributo cls
        scope = getattr(self, 'scope', {'user': {'id': None}})
        # print(func)
        # print('scope', scope)
        print('dec id: ', scope['user'].id)
        # print(scope['user'])
        if scope['user'].id != None:
            return await func(self, *args, **kwargs)
        else:
            # print('usuario no activo')
            return asyncio.sleep(1)
    return wrapper

def token_required(func):
    """
    buscar usuario y asignar (notificar error)
    notas:
    - solo para metodo receive asyncwebsocketconsumer
    - token en solicitud
    - consumir posee propieadad para notificar error
    """
    @functools.wraps(func)
    async def wrapper(self, text_data: str, *args, **kwargs):
        # optener atributo cls
        scope = getattr(self, 'scope', {'user': {'id': None}})
        # print(func)
        # print('scope', scope)
        print('request dec id: ', scope['user'].id)
        # print(scope['user'])
        if scope['user'].id != None:
            return await func(self, text_data, *args, **kwargs)
        else:
            text_data_json: Dict['str', Any] = json.loads(text_data)
            channel_name = getattr(self, 'channel_name')
            print(channel_name)
            channel_layer = None

            if 'token' not in text_data_json:
                channel_layer = get_channel_layer()
                return await channel_layer.send(channel_name, {
                    "type": getattr(self, 'error_event'),
                    'code': 401,
                    'details': 'user or token no exist',
                })

            user: Union[User, None] = await user_token(text_data_json['token'])
            if user != None:
                # asignar atributo cls
                scope['user'] = user
                setattr(self, 'scope', scope)
                return await func(self, text_data, *args, **kwargs)
            else:
                # print('fallo autenticacion')
                channel_layer = get_channel_layer()
                return await channel_layer.send(channel_name, {
                    "type": getattr(self, 'error_event'),
                    'code': 401,
                    'details': 'user or token no exist',
                })
    return wrapper
