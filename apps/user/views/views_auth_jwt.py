"""
Vistas autenticacion de usuarios
"""

import jwt
from django.conf import settings

# from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.authentication import TokenAuthentication
from apps.user.serializers import AuthTokenSerializer, UserHeavySerializer


class AuthJwtHS256Token(ObtainAuthToken):
    """
    ...
    """

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        ...
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_serializer = UserHeavySerializer(user)
        token, _ = Token.objects.get_or_create(user=user)
        key = settings.KEY_HS256
        encoded_jwt = jwt.encode(
            {"token": token.key, "user": user_serializer.data}, key, algorithm="HS256"
        )
        return Response(encoded_jwt.decode("UTF-8"), status=status.HTTP_200_OK)


class CurrentUserJwtView(APIView):
    """
    ...
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        ...
        """
        user_serializer = UserHeavySerializer(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK,)
