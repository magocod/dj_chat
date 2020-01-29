"""
Rutas websockets
"""

# Django
# from channels.auth import AuthMiddlewareStack
# from django.conf import settings
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator

# local Django
from chat.routing import websocket_urlpatterns as wschat
from user.routing import websocket_urlpatterns as wsauth
from user.middleware import AnonymousAuthMiddleware, JWTAuthMiddleware

# JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(
# AnonymousAuthMiddleware(inner))

# concatenar rutas
WS_URLS = wschat + wsauth

application = ProtocolTypeRouter({
    "websocket": OriginValidator(
        # rutas y autenticion
        JWTAuthMiddleware(
            AnonymousAuthMiddleware(
                URLRouter(
                    WS_URLS,
                ),
            )
        ),
        # origenes permitidos
        # settings.CORS_ORIGIN_WHITELIST,
        ['*'],
    ),
})
