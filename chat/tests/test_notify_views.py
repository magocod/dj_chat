"""
...
"""

# standard library
import json
from typing import Any, Dict

# third-party
import pytest

# permitir acceso a db
pytestmark = pytest.mark.django_db

@pytest.mark.notifications_views
def test_get_notifytestview(admin_client):
    """
    prueba de views
    """

    # Test call view
    response = admin_client.get('/api/notify/test/')
    assert response == None
