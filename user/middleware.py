"""
...
"""

# third-party
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token

# Django
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.db import close_old_connections


class WebsocketDenier(AsyncWebsocketConsumer):
    """
    Simple application which denies all requests to it.
    """

    async def connect(self):
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

        print(scope)
        if 'user' in scope:
            # print('user jwt')
            return self.inner(scope)

        # set anonymoususer
        # print('user anonymous')
        user = AnonymousUser()
        return self.inner(dict(scope, user=user))


class JWTAuthMiddleware():
    """
    Token route authorization
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # Close old database connections to
        # prevent usage of timed out connections
        close_old_connections()

        path = scope['path']
        pathlist = path.split('/')
        # print(path)
        # print(pathlist)
        if 'jwt' in pathlist:
            # print('auth jwt')
            return self.decode_jwt(
                scope,
                pathlist[len(pathlist) - 2]  # jwt token
            )

        # print('auth anonymous')
        return self.inner(scope)

    def decode_jwt(self, scope, urltoken: str):
        # print(urltoken)
        try:
            decoded = jwt.decode(
                urltoken,
                settings.KEY_HS256,
                algorithms='HS256'
            )
            tk = Token.objects.get(key=decoded['token'])
            # print(tk.user)
            user = User.objects.get(id=tk.user_id)
            return self.inner(dict(scope, user=user))
        except Exception as e:
            print(e)
            # return self.inner(scope)
            # Deny the connection
            return WebsocketDenier(scope)
