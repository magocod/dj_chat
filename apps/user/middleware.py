"""
...
"""

import asyncio
import json

import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

User = get_user_model()


class WebsocketDenier(AsyncWebsocketConsumer):
    """
    Simple application which denies all requests to it.
    """

    async def connect(self):
        # print('scope', self.scope)
        await self.accept()
        await self.send(text_data=json.dumps(self.scope["exception"]))
        await asyncio.sleep(1)
        await self.close()


class AnonymousAuthMiddleware:
    """
    anonymous users
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):

        # Close old database connections to
        # prevent usage of timed out connections
        close_old_connections()

        # print(scope)
        if "user" in scope:
            # print('user jwt')
            return self.inner(scope)

        # set anonymoususer
        # print('user anonymous')
        user = AnonymousUser()
        return self.inner(dict(scope, user=user))


class JWTAuthMiddleware:
    """
    Token route authorization
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # Close old database connections to
        # prevent usage of timed out connections
        close_old_connections()

        path = scope["path"]
        pathlist = path.split("/")
        # print(path)
        # print(pathlist)
        if "jwt" in pathlist:
            # print('auth jwt')
            # result (dict or User)
            result = self.decode_jwt(pathlist[len(pathlist) - 2])  # jwt token

            if isinstance(result, dict):
                # print('result', result)
                scope["exception"] = result
                return WebsocketDenier(scope)

            return self.inner(dict(scope, user=result))

        # print('auth anonymous')
        return self.inner(scope)

    def decode_jwt(self, urltoken: str):
        # print(urltoken)
        try:
            decoded = jwt.decode(urltoken, settings.KEY_HS256, algorithms="HS256")
            tk = Token.objects.get(key=decoded["token"])
            # print(tk.user)
            user = User.objects.get(id=tk.user_id)
            return user

        except Exception as e:
            # print('Exception', e)
            # print('name', e.__class__.__name__)
            # Deny the connection
            return {"message": "authentication failed", "exception": str(e)}
