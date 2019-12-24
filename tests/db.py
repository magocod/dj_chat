"""
...
"""

from channels.db import database_sync_to_async


@database_sync_to_async
def async_count_db(model):
    """
    ...
    """
    return model.objects.count()


@database_sync_to_async
def async_count_filter_db(model, **kwargs):
    """
    ...
    """
    return model.objects.filter(**kwargs).count()


@database_sync_to_async
def async_create_model(model, **kwargs):
    """
    ...
    """
    return model.objects.create(**kwargs)


@database_sync_to_async
def async_bulk_create_model(model, instances):
    """
    ...
    """
    return model.objects.bulk_create(instances)


@database_sync_to_async
def async_get_model(model, many=False, **kwargs):
    """
    ...
    """
    if many:
        return model.objects.all()
    return model.objects.get(**kwargs)


@database_sync_to_async
def async_filter_models(model, **kwargs):
    """
    ...
    """
    return model.objects.filter(**kwargs)


@database_sync_to_async
def async_delete_models(model, **kwargs):
    """
    ...
    """
    return model.objects.filter(**kwargs).delete()
