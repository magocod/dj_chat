"""
...
"""

from apps.chat.models import Message, Room

from django.contrib import admin

admin.site.register(Message)
admin.site.register(Room)
