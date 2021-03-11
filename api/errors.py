from api.response import HttpCodes


class ApiException(Exception):
    """
    Base class to our API errors & exceptions.
    """
    def __init__(self, error_msg, error_http_code=HttpCodes.BAD_REQUEST):

        self.error_msg = error_msg
        self._error_http_code = error_http_code

    def __str__(self):
        """
        Returns the string representation of the api exception class.

        Returns:
            str: api response as a string.
        """
        if self._is_client_error():
            return f"Client error: {self.error_msg}, error code: {self._error_http_code}"
        else:
            return f"Server error: {self.error_msg}, error code: {self._error_http_code}"

    def _is_client_error(self):
        """
        Checks whether the the error that occurred is a client error.

        Returns:
            bool: True if the error is client error, False otherwise.
        """
        if 400 <= self._error_http_code < 500:
            return True
        return False

    @property
    def error_http_code(self):
        return self._error_http_code


class InvalidInputData(ApiException):

    def __init__(self, arg, error_http_code=HttpCodes.BAD_REQUEST):
        super().__init__(error_msg=f"{arg} was not found on the request body", error_http_code=error_http_code)





