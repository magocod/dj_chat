"""
user tests edit profile photo
"""

import os

import pytest
from django.contrib.auth import get_user_model

from apps.user.serializers import UserHeavySerializer

# from PIL import Image


User = get_user_model()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pytestmark = [pytest.mark.django_db, pytest.mark.users_views]


@pytest.mark.users_photo
def test_user_update_photo(admin_client):
    """
    ...
    """

    user_id: int = 1
    origin_user = UserHeavySerializer(User.objects.get(id=user_id)).data

    file_path = (os.path.dirname(__file__)) + "/images/data_lab_480.png"
    # im = Image.open(file_path);
    im = open(file_path, "rb")
    # print(im)

    request = {
        "photo": im,
    }

    response = admin_client.post("/api/user/update_photo/", request, format="multipart")
    updated_user = UserHeavySerializer(User.objects.get(id=user_id)).data

    print(response.data)
    assert response.status_code == 200
    # print(updated_user['photo'])
    assert origin_user != updated_user
    assert response.data == updated_user


@pytest.mark.users_photo
def test_user_validate_update_photo(admin_client):
    """
    ...
    """

    user_id: int = 1
    origin_user = UserHeavySerializer(User.objects.get(id=user_id)).data

    request = {
        "photo": False,
    }

    response = admin_client.post("/api/user/update_photo/", request, format="multipart")
    not_updated_user = UserHeavySerializer(User.objects.get(id=user_id)).data

    # print(response.data)
    assert response.status_code == 422
    assert origin_user == not_updated_user
