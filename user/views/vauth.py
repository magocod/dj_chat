"""
Vistas autenticacion de usuarios
"""

# third-party
import jwt

# Django
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# local Django
from user.serializers import AuthTokenSerializer, EmailSerializer, UserHeavySerializer


class CustomAuthToken(ObtainAuthToken):
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
        return Response(
            {"token": token.key, "user": user_serializer.data},
            status=status.HTTP_200_OK,
        )


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
        return Response(encoded_jwt, status=status.HTTP_200_OK)


class EmailView(APIView):
    """
    ...
    """

    permission_classes = (AllowAny,)
    serializer = EmailSerializer

    def get_object(self, user_email: str):
        """
        ...
        """
        try:
            return User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        """
        ...
        """
        response = self.serializer(data=request.data)
        if response.is_valid():
            self.get_object(response.validated_data["email"])
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    ...
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        ...
        """
        Token.objects.get(key=request.auth.key).delete()
        return Response(status=status.HTTP_200_OK)
