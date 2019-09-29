"""
Edicion de usuarios
"""

# standard library
from typing import Union

# third-party
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.http import Http404
from django.contrib.auth.models import User

# local Django
from apps.user.serializers import UserSerializer, UserRegisterSerializer, UserHeavySerializer

class VUserList(APIView):
    """
    ...
    """
    permission_classes = (IsAdminUser,)
    serializer = UserHeavySerializer

    def serialize_user(self, pk):
        """
        ...
        """
        try:
            user = User.objects.get(pk=pk)
            res = self.serializer(user)
            return res.data
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        """
        ...
        """
        response = self.serializer(User.objects.all().order_by('id'), many=True)
        return Response(response.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        ...
        """
        response = UserRegisterSerializer(data=request.data)
        if response.is_valid():
            iduser: int = response.save()
            res = self.serialize_user(pk=iduser)
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)

class VUserDetail(APIView):
    """
    ...
    """
    permission_classes = (IsAdminUser,)
    serializer = UserSerializer

    def get_object(self, pk_user: Union[int, str]):
        """
        ...
        """
        try:
            return User.objects.get(pk=pk_user)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk: Union[int, str], format=None):
        """
        ...
        """
        user = self.get_object(pk)
        response = UserHeavySerializer(user)
        return Response(response.data, status=status.HTTP_200_OK)

    def put(self, request, pk: Union[int, str], format=None):
        """
        ...
        """
        user = self.get_object(pk)
        response = self.serializer(user, data=request.data)
        if response.is_valid():
            result = response.save()
            res = UserHeavySerializer(result)
            return Response(res.data, status=status.HTTP_200_OK)
        else:
            return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: Union[int, str], format=None):
        """
        ...
        """
        user = self.get_object(pk)
        # value = user.id
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
