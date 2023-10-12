from rest_framework import exceptions
from rest_framework.status import HTTP_400_BAD_REQUEST


class InvalidRequestData(exceptions.APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "invalid request data"