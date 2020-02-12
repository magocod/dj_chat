"""
ASGI config for dj3 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_chat.settings')
# application = get_asgi_application()

# ASGI entrypoint. Configures Django and then runs the application
# defined in the ASGI_APPLICATION setting.

import os

import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_chat.settings")
# os.environ['ASGI_THREADS'] = "4"
django.setup()

application = get_default_application()
