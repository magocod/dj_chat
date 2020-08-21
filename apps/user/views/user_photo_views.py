"""
Edicion de usuarios (perfil)
"""

# from django.contrib.auth import authenticate
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.serializers import (
    PictureSerializer,
    UserHeavySerializer,
    UserPhotoSerializer,
)


class UserUpdatePhotoView(APIView):
    """
    ...
    """

    permission_classes = (IsAuthenticated,)
    serializer = UserPhotoSerializer
    response_serializer = UserHeavySerializer

    def get(self, request):
        print(request.user.photo.width)
        print(request.user.photo.url)
        # path = default_storage.save('example/file.txt', ContentFile(b'new content'))
        url_data = PictureSerializer(request.user)
        return Response(url_data.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        user modifies his current photo
        """

        response = self.serializer(request.user, data=request.data)
        if response.is_valid():
            # print(response.validated_data);
            user = response.save()
            # print(user)
            serializer_user = UserHeavySerializer(user)
            return Response(serializer_user.data, status=status.HTTP_200_OK)
            # return Response(status=status.HTTP_200_OK)

        return Response(response.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
