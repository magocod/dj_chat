"""
Rutas websockets
"""

# Django
# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator

# local Django
from chat.routing import websocket_urlpatterns as wschat
from user.middleware import TokenAuthMiddleware


# concatenar rutas
WS_URLS = wschat

application = ProtocolTypeRouter({
    "websocket": OriginValidator(
        # rutas y autenticion
        TokenAuthMiddleware(
            URLRouter(
                WS_URLS,
            ),
        ),
        # origenes permitidos
        # ['localhost:8080', 'django-237201.firebaseapp.com',],
        ['*'],
    ),
})
