"""
test list users
"""

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.user.serializers import UserHeavySerializer

User = get_user_model()


# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.users_views]


@pytest.mark.users_list
def test_get_all_user(admin_client):
    """
    ...
    """
    response = admin_client.get("/api/users/?page=1")
    serializer = UserHeavySerializer(
        User.objects.all()[: settings.REST_FRAMEWORK["PAGE_SIZE"]], many=True
    )
    assert response.status_code == 200
    assert response.data["data"] == serializer.data
    assert response.data["total"] == User.objects.count()


@pytest.mark.users_list
def test_list_users_only_for_super_users(staff_client):
    """
    ...
    """
    response = staff_client.get("/api/users/")
    assert response.status_code == 403
