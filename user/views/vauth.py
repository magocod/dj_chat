"""
Vistas autenticacion de usuarios
"""

# third-party
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Django
from django.http import Http404
from django.contrib.auth.models import User

# local Django
from apps.user.serializers import AuthTokenSerializer, EmailSerializer

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
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'staff_status': user.is_staff,
            'super_user': user.is_superuser,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'date_joined': user.date_joined,
            'id': user.id,
        }, status=status.HTTP_200_OK)

class VEmail(APIView):
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
        except:
            raise Http404

    def post(self, request, format=None):
        """
        ...
        """
        response = self.serializer(data=request.data)
        if response.is_valid():
            self.get_object(response.validated_data['email'])
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class VLogout(APIView):
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
