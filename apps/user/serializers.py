"""
Serilizers Users
"""

from typing import Any, Dict, Tuple

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers

# from rest_framework.exceptions import APIException

User = get_user_model()

# class GroupSerializer(serializers.ModelSerializer):
#     """
#     ...
#     """
#     class Meta:
#         model = Group
#         fields: Tuple[str] = ('url', 'name')


class PermissionSerializer(serializers.ModelSerializer):
    """
    ...
    """

    class Meta:
        model = Permission
        fields: Tuple[str] = ("id", "content_type_id", "codename", "name")


class UserSerializer(serializers.ModelSerializer):
    """
    ...
    """

    class Meta:
        model = User
        fields: Tuple[str] = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
        )


class UserHeavySerializer(serializers.ModelSerializer):
    """
    ...
    """

    user_permissions = PermissionSerializer(many=True)

    class Meta:
        model = User
        fields: Tuple[str] = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "date_joined",
            "user_permissions",
            "is_superuser",
            "photo",
        )


class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    """
    ...
    """

    class Meta:
        model = User
        fields: Tuple[str] = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_staff",
        )

    def create(self, validated_data: Dict[str, Any]) -> int:
        """
        ...
        """
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user.id


class EmailSerializer(serializers.Serializer):
    """
    ...
    """

    email = serializers.EmailField()


class PasswordSerializer(serializers.Serializer):
    """
    modify a user's password by id
    """

    user_id = serializers.IntegerField()
    password = serializers.CharField(max_length=30)


class PasswordResetSerializer(serializers.Serializer):
    """
    the user modifies his password
    """

    old_password = serializers.CharField(max_length=30)
    new_password = serializers.CharField(max_length=30)


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
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                userdata = User.objects.get(email__exact=email)
            except Exception:
                msg = "User no exist."
                # raise APIException(msg)
                raise serializers.ValidationError(msg, code="authorization")

            user = authenticate(username=userdata.username, password=password)
            # print(userdata)

            if user:
                pass
            else:
                if not userdata.is_active:
                    msg = "User account is disabled."
                    raise serializers.ValidationError(
                        msg, code="authorization",
                    )
                    # raise APIException(msg)
                else:
                    msg = "Unable to log in with provided credentials."
                    # raise APIException(msg, status.HTTP_400_BAD_REQUEST)
                    raise serializers.ValidationError(
                        msg, code="authorization",
                    )
        else:
            msg = 'Must include "email" and "password".'
            # raise APIException(msg)
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data


class UserPhotoSerializer(serializers.ModelSerializer):
    """
    update user photo
    """

    photo = serializers.ImageField()

    class Meta:
        model = User
        fields = ("photo",)


class PictureSerializer(serializers.ModelSerializer):
    """[summary]

    [description]

    Extends:
        serializers.ModelSerializer

    Variables:
        photo_url {[type]} -- [description]
    """

    photo_url = serializers.SerializerMethodField("get_photo_url")

    class Meta:
        model = User
        fields = ("photo", "photo_url")

    def get_photo_url(self, obj):
        # request = self.context.get("request")
        return obj.photo.url
