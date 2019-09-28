"""
Rutas websockets
"""

# Django
# from django.conf import settings
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator


# concatenar rutas
WS_URLS = []

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
