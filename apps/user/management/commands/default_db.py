"""
ejecutar comando creacion de usuarios por defecto
"""

from django.core.management.base import BaseCommand

from apps.user.database.seeders import user_list


class Command(BaseCommand):
    """
    ...
    """

    def handle(self, *args, **options):
        """
        ...
        """
        user_list()
