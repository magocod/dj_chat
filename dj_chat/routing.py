"""
Rutas websockets
"""

# Django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator

# local Django
from chat.routing import websocket_urlpatterns as wschat


# concatenar rutas
WS_URLS = wschat

application = ProtocolTypeRouter({
    "websocket": OriginValidator(
        # rutas y autenticion
        AuthMiddlewareStack(
            URLRouter(
                WS_URLS,
            ),
        ),
        # origenes permitidos
        # ['localhost:8080', 'django-237201.firebaseapp.com',],
        ['*'],
    ),
})
