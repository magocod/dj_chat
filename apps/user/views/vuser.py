"""
Edicion de usuarios
"""

from typing import Union

from django.contrib.auth import get_user_model

# from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status

# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.permissions import IsSuperUser
from apps.user.serializers import (
    PasswordSerializer,
    UserHeavySerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from dj_chat.views import CustomPagination

# from rest_framework.pagination import PageNumberPagination


User = get_user_model()


class UserListView(APIView, CustomPagination):
    """
    ...
    """

    permission_classes = (IsSuperUser,)
    serializer = UserHeavySerializer

    def serialize_user(self, pk):
        """
        ...
        """
        user = User.objects.get(pk=pk)
        serializer = self.serializer(user)
        return serializer.data

    def get(self, request, format=None):
        """
        ...
        """
        queryset = User.objects.all().order_by("id")
        results = self.paginate_queryset(queryset, request)
        serializer = self.serializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        ...
        """
        response = UserRegisterSerializer(data=request.data)
        if response.is_valid():
            user_id: int = response.save()
            res = self.serialize_user(pk=user_id)
            return Response(res, status=status.HTTP_201_CREATED)

        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    ...
    """

    permission_classes = (IsSuperUser,)
    serializer = UserSerializer

    @staticmethod
    def get_object(user_pk):
        """
        hello
        """
        try:
            return User.objects.get(pk=user_pk)
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

        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: Union[int, str], format=None):
        """
        ...
        """
        user = self.get_object(pk)

        if user.id == request.user.id:
            return Response("can't delete himself", status=status.HTTP_400_BAD_REQUEST,)

        if user.is_superuser:
            return Response(
                "super users cannot be deleted", status=status.HTTP_400_BAD_REQUEST,
            )

        # if user.is_staff:
        #     if not request.user.is_superuser:
        #         return Response(
        #             'user cannot delete administrators',
        #             status=status.HTTP_400_BAD_REQUEST,
        #         )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserModifyPasswordView(APIView):
    """
    Modify User Password
    """

    permission_classes = (IsSuperUser,)
    serializer = PasswordSerializer

    @staticmethod
    def get_object(pk):
        """
        ...
        """
        try:
            return User.objects.get(pk=pk)
        except Exception as e:
            print(e)
            raise Http404

    def post(self, request, format=None):
        """
        ...
        """
        response = self.serializer(data=request.data)
        if response.is_valid():
            user = self.get_object(response.data["user_id"])

            if user.is_superuser is True:
                return Response(
                    "editing of superuser passwords is not allowed",
                    status=status.HTTP_403_FORBIDDEN,
                )

            user.set_password(response.data["password"])
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)
