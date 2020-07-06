"""
...
"""

from typing import Any, Dict

import jwt

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

jwt_decoded = Dict[str, Any]


class TokenAuthentication(BaseAuthentication):
    """
    encoded token authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = "Bearer"
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token

        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        # [keyword, token]
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                "Invalid token header. Token string" + " should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        try:
            # token = auth[1]
            # print(token)
            token = auth[1].decode()
            # auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should"
                + "not contain invalid characters."
            )
            raise exceptions.AuthenticationFailed(msg)

        decoded: jwt_decoded = {}
        try:
            decoded = jwt.decode(token, settings.KEY_HS256, algorithms="HS256")
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

        # print('jwt', decoded)
        if "token" not in decoded:
            raise exceptions.AuthenticationFailed("invalid decoded token (token)")

        if "user" not in decoded:
            raise exceptions.AuthenticationFailed("invalid decoded token (user)")

        return self.authenticate_credentials(decoded["token"])

    def authenticate_credentials(self, key: str):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword
