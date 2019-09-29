"""
ejecutar comando creacion de usuarios por defecto
"""

# Django
from django.core.management.base import BaseCommand

# local Django
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
