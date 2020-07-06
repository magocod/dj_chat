"""
...
"""

from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
    ...
    """

    name = "apps.chat"

    def ready(self):
        pass
        # import chat.db.signals # noqa
