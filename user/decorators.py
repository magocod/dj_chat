"""
Decoradores verificacion de usuarios en consumidores
"""

# standard library
import asyncio
import functools
import json
from typing import Any, Dict, Union

# third-party
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
# Django
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authtoken.models import Token


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
        scope = getattr(self, 'scope')
        user = AnonymousUser()
        if 'user' in scope:
            user = scope['user']

        if user.id != None:
            return await func(self, *args, **kwargs)
        else:
            # print('usuario no activo')
            return await asyncio.sleep(1)
    return wrapper

def token_required(func):
    """
    buscar usuario y asignar (notificar error)
    notas:
    - solo para metodo receive asyncwebsocketconsumer
    - token en solicitud
    """
    @functools.wraps(func)
    async def wrapper(self, text_data: str, *args, **kwargs):
        scope = getattr(self, 'scope')
        user = AnonymousUser()
        if 'user' in scope:
            user = scope['user']

        print('request dec id: ', user.id)
        if user.id != None:
            return await func(self, text_data, *args, **kwargs)
        else:
            text_data_json: Dict['str', Any] = json.loads(text_data)
            channel_name = getattr(self, 'channel_name')
            print(channel_name)
            channel_layer = None

            if 'token' not in text_data_json:
                return await self.send(text_data=json.dumps({
                    'code': 401,
                    'details': 'Authentication credentials were not provided',
                }))

            user: Union[User, None] = await user_token(text_data_json['token'])
            if user != None:
                # asignar atributo cls
                scope['user'] = user
                setattr(self, 'scope', scope)
                return await func(self, text_data, *args, **kwargs)
            else:
                return await self.send(text_data=json.dumps({
                    'code': 401,
                    'details': 'user or token no exist',
                }))
                
    return wrapper

def token_admin_required(func):
    """
    buscar usuario y asignar (notificar error)
    notas:
    - solo para metodo receive asyncwebsocketconsumer
    - token en solicitud
    """
    @functools.wraps(func)
    async def wrapper(self, text_data: str, *args, **kwargs):
        scope = getattr(self, 'scope')
        print('request dec id: ', scope['user'].id)
        user = AnonymousUser()
        if 'user' in scope:
            user = scope['user']

        if user.id != None:
            return await func(self, text_data, *args, **kwargs)
        else:
            text_data_json: Dict['str', Any] = json.loads(text_data)
            channel_name = getattr(self, 'channel_name')
            print(channel_name)
            channel_layer = None

            if 'token' not in text_data_json:
                return await self.send(text_data=json.dumps({
                    'code': 401,
                    'details': 'Authentication credentials were not provided',
                }))

            user: Union[User, None] = await user_token(text_data_json['token'])
            if user != None:

                if user.is_staff == False:
                    return await self.send(text_data=json.dumps({
                        'code': 401,
                        'details': 'user does not have permissions',
                    }))

                # asignar atributo cls
                scope['user'] = user
                setattr(self, 'scope', scope)
                return await func(self, text_data, *args, **kwargs)
            else:
                return await self.send(text_data=json.dumps({
                    'code': 401,
                    'details': 'user or token no exist',
                }))
    return wrapper
