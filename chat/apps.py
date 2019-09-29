"""
...
"""

from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
    ...
    """
    name: str = 'chat'

    def ready(self):
        import chat.db.signals # noqa
