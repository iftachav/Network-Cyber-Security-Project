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


class ResourceNotFoundError(ApiException):

    def __init__(self, resource, resource_type="username", error_http_code=HttpCodes.NOT_FOUND):
        super().__init__(
            error_msg=f"resource {resource_type} {resource} was not found", error_http_code=error_http_code
        )


class DatabaseOperationError(ApiException):

    def __init__(self, error_msg, error_http_code=HttpCodes.INTERNAL_SERVER_ERROR):
        super().__init__(error_msg=error_msg, error_http_code=error_http_code)


class DatabaseInsertionError(DatabaseOperationError):
    pass


class DatabaseDeletionError(DatabaseOperationError):
    pass


class BadEmailError(ApiException):

    def __init__(self, email, error_http_code=HttpCodes.BAD_REQUEST):
        super().__init__(error_msg=f"email {email} is not in a valid form", error_http_code=error_http_code)


class InvalidPasswordProvided(ApiException):
    def __init__(self, error_http_code=HttpCodes.BAD_REQUEST):
        """
        maybe it would be better not to mention which password failed for each user due to security reasons
        """
        super().__init__(error_msg="password/username is invalid", error_http_code=error_http_code)
