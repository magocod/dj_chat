"""
...
"""

from django.urls import path

from apps.user.consumers.cauth import AuthConsumer

websocket_urlpatterns = [
    path("ws/auth/jwt/<str:jwt>/", AuthConsumer),
]
