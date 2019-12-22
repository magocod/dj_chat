"""
Importador usuarios
"""

# standard library
from typing import Any, Dict, Tuple

# Django
from django.contrib.auth.models import User
# third-party
from rest_framework.authtoken.models import Token

USERS: Tuple[Dict[str, Any]] = (
    {
        'username': 'generic_admin',
        'email': 'admin@django.com',
        'password': '123',
        'first_name': 'admin',
        'last_name': 'Generic',
        'staff': True,
        'super': True,
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6120',
    },
    {
        'username': 'generic_user',
        'email': 'user@django.com',
        'password': '123',
        'first_name': 'user',
        'last_name': 'Generic',
        'staff': False,
        'super': False,
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6130',
    },
    {
        'username': 'generic_superuser',
        'email': 'superuser@django.com',
        'password': '123',
        'first_name': 'super',
        'last_name': 'Generic',
        'staff': True,
        'super': True,
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6140',
    },
    {
        'username': 'generic_userstaff',
        'email': 'userstaff@django.com',
        'password': '123',
        'first_name': 'staff',
        'last_name': 'Generic',
        'staff': True,
        'super': False,
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6150',
    },
    {
        'username': 'user_staff',
        'email': 'userstaff2@django.com',
        'password': '123',
        'first_name': 'staff',
        'last_name': 'Generic',
        'staff': True,
        'super': False,
        'token': '20fd382ed9407b31e1d5f928b5574bb4bffe6160',
    },
)

def user_list():
    """
    migrar en db usuarios con un token
    """
    for values in USERS:
        user = User.objects.create_user(
            values['username'],
            values['email'],
            values['password']
        )
        user.first_name = values['first_name']
        user.last_name = values['last_name']
        user.is_staff = values['staff']
        user.is_superuser = values['super']
        user.save()
        Token.objects.create(key=values['token'], user_id=user.id)
    
    print('users created')
