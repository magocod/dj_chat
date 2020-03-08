"""
Rutas websockets
"""


# from channels.auth import AuthMiddlewareStack
# from django.conf import settings
from channels.routing import ProtocolTypeRouter, URLRouter

# Django
from channels.security.websocket import OriginValidator

# local Django
from chat.routing import websocket_urlpatterns as wschat
from user.middleware import AnonymousAuthMiddleware, JWTAuthMiddleware
from user.routing import websocket_urlpatterns as wsauth

# JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(
# AnonymousAuthMiddleware(inner))

# concatenar rutas
WS_URLS = wschat + wsauth

application = ProtocolTypeRouter(
    {
        "websocket": OriginValidator(
            # rutas y autenticion
            JWTAuthMiddleware(AnonymousAuthMiddleware(URLRouter(WS_URLS,),)),
            # origenes permitidos
            # settings.CORS_ORIGIN_WHITELIST,
            ["*"],
        ),
    }
)
