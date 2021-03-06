"""
...
"""

from channels.db import database_sync_to_async


@database_sync_to_async
def create_event_message(id: int, operation: str, model, serializer):
    """
    retrieve an element of db
    serialize and return it as a sockect response
    """
    instance = model.objects.get(id=id)
    serializer_instance = serializer(instance)
    return {
        "method": operation,
        "data": serializer_instance.data,
    }


@database_sync_to_async
def create_event_list_message(model, serializer):
    """
    retrieve an element of db
    serialize and return it as a sockect response
    """
    instances = model.objects.all()
    serializer_instance = serializer(instances, many=True)
    return {
        "method": "R",
        "data": serializer_instance.data,
    }


@database_sync_to_async
def create_event_filter_list_message(model, serializer, **kwargs):
    """
    retrieve an element of db
    serialize and return it as a sockect response
    """
    instances = model.objects.filter(**kwargs)
    serializer_instance = serializer(instances, many=True)
    return {
        "method": "R",
        "data": serializer_instance.data,
    }
