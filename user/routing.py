"""
...
"""

# Django
from django.urls import path

# local Django
from user.consumers.cauth import AuthConsumer

websocket_urlpatterns = [
    path("ws/auth/jwt/<str:jwt>/", AuthConsumer),
]
