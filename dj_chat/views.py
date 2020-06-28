"""
Provides an APIView class that is the base of all views in REST framework.
"""

# from django.conf import settings

from rest_framework import exceptions, status, pagination
from rest_framework.response import Response
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


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        """[summary]

        [description]

        Arguments:
            data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        return Response(
            {
                "total": self.page.paginator.count,
                "per_page": self.page_size,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )
