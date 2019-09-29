"""
Authenticacion pruebas
"""

# standard library
from typing import Dict, Any

# third-party
from rest_framework.authtoken.models import Token

# Django
from django.contrib.auth.models import User

def create_user(staff: bool = False) -> Dict[str, Any]:
    """
    [creacion de usuarios]

    Arguments:
        staff {bol} -- [description]

    Returns:
        dicc [user, token] -- [description]
    """
    user = User.objects.create_user(
        'usertest',
        'user@test.com',
        '123',
    )
    # admin
    user.is_staff = staff
    user.save()
    Token.objects.get_or_create(user=user)
    # auth token
    token = Token.objects.get(user__username=user.username)
    return {'user': user, 'token': token}
