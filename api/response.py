from flask import make_response, jsonify
from flask import request


class HttpMethods:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


class HttpCodes(object):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    MULTI_STATUS = 207
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    DUPLICATE = 409
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class ApiResponse(object):
    """
    Class that represents the API response to the client.
    """
    def __init__(self, response_body, http_status_code=HttpCodes.OK):

        self._response_body = response_body
        self._http_status_code = http_status_code

    @property
    def full_api_response(self):
        return make_response(jsonify(self._response_body), self._http_status_code)


class ErrorResponse(ApiResponse):
    """
    class that represents error responses to the client.
    """
    def __init__(self, err_msg, http_error_code):

        error_body_response = {
            "error": {
                "message": err_msg,
                "code": http_error_code
            }
        }
        super().__init__(response_body=error_body_response, http_status_code=http_error_code)


def response_decorator(code):
    """
    Decorator to execute all the API services implementations and parse a valid response to them.

    Args:
        code (int): http code that should indicate about success.
    """
    def first_wrapper(func):
        """
        wrapper to get the service function.

        Args:
            func (Function): a function object representing the API service function.
        """
        def second_wrapper(*args, **kwargs):
            """
            Args:
                args: function args
                kwargs: function kwargs

            Returns:
                Response: flask api response.
            """
            try:
                return ApiResponse(response_body=func(*args, **kwargs), http_status_code=code).full_api_response
            except Exception as e:
                return ErrorResponse(str(e), e.error_http_code).full_api_response
        return second_wrapper
    return first_wrapper

