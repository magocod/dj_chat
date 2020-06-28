"""
Provides an APIView class that is the base of all views in REST framework.
"""

from rest_framework import exceptions, status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """[summary]

    [description]
    Call REST framework's default exception handler first,
    to get the standard error response.

    Arguments:
        exc {[type]} -- [description]
        context {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    response = exception_handler(exc, context)

    if isinstance(exc, exceptions.ValidationError):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    # print(response.status_code)

    return response
