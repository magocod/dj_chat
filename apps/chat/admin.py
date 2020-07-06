"""
...
"""

# Django
from django.contrib import admin

# local Django
from chat.models import Message, Room

admin.site.register(Message)
admin.site.register(Room)
