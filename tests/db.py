"""
...
"""

from channels.db import database_sync_to_async


@database_sync_to_async
def count_db(model):
    """
    ...
    """
    return model.objects.count()
