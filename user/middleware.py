"""
...
"""

from django.contrib.auth.models import AnonymousUser
# Django
from django.db import close_old_connections


class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):

        # Close old database connections to
        # prevent usage of timed out connections
        close_old_connections()

        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        # print(scope)
        user = AnonymousUser()

        # Return the inner application directly and let it run everything else
        return self.inner(dict(scope, user=user))
