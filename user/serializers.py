"""
Serilizadores Usuarios
"""

# standard library
from typing import Any, Dict, Tuple

# Django
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission, User
# third-party
from rest_framework import serializers

# from rest_framework.exceptions import APIException


class GroupSerializer(serializers.ModelSerializer):
    """
    ...
    """
    class Meta:
        model = Group
        fields: Tuple[str] = ('url', 'name')


class PermissionSerializer(serializers.ModelSerializer):
    """
    ...
    """
    class Meta:
        model = Permission
        fields: Tuple[str] = ('id', 'content_type_id', 'codename', 'name')


class UserSerializer(serializers.ModelSerializer):
    """
    ...
    """
    class Meta:
        model = User
        fields: Tuple[str] = (
            'id', 'username', 'email',
            'first_name', 'last_name', 'is_staff',
        )


class UserHeavySerializer(serializers.ModelSerializer):
    """
    ...
    """
    user_permissions = PermissionSerializer(many=True)

    class Meta:
        model = User
        fields: Tuple[str] = (
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_staff', 'date_joined',
            'user_permissions', 'is_superuser',
        )


class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    """
    ...
    """
    class Meta:
        model = User
        fields: Tuple[str] = (
            'id', 'username', 'password',
            'email', 'first_name', 'last_name',
            'is_staff',
        )

    def create(self, validated_data: Dict[str, Any]) -> int:
        """
        ...
        """
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user.id


class EmailSerializer(serializers.Serializer):
    """
    ...
    """
    email = serializers.EmailField()


class AuthTokenSerializer(serializers.Serializer):
    """
    ...
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=40)

    def validate(self, data) -> Any:
        """
        ...
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                userdata = User.objects.get(email__exact=email)
            except Exception:
                msg = ('User no exist.')
                # raise APIException(msg)
                raise serializers.ValidationError(msg, code='authorization')

            user = authenticate(username=userdata.username, password=password)
            # print(userdata)

            if user:
                pass
            else:
                if not userdata.is_active:
                    msg = ('User account is disabled.')
                    raise serializers.ValidationError(
                        msg,
                        code='authorization',
                    )
                    # raise APIException(msg)
                else:
                    msg = ('Unable to log in with provided credentials.')
                    # raise APIException(msg, status.HTTP_400_BAD_REQUEST)
                    raise serializers.ValidationError(
                        msg,
                        code='authorization',
                    )
        else:
            msg = ('Must include "email" and "password".')
            # raise APIException(msg)
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
