"""
...
"""

# local Django
from chat.models import Message, Room
# Django
from django.contrib import admin

admin.site.register(Message)
admin.site.register(Room)
