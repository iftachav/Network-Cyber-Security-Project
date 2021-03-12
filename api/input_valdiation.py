from flask import request
from email_validator import validate_email, EmailNotValidError

from api.errors import InvalidInputData, BadEmailError


def validate_input_data(*arguments, create=True):
    """
    Validates that the provided arguments are indeed a part of the json body request.

    Note: in case all the arguments are valid, this decorator just executes the decorated function.

    Args:
        arguments (list[str]): all the keys that should be in the json request.
        create (bool): True if decorating a function which creates a new resource.
    """
    def function_wrapper(func):

        def arguments_wrapper(self, *func_args, **func_kwargs):

            input_data = request.json

            if create:
                for arg in arguments:
                    if arg not in input_data:
                        raise InvalidInputData(arg=arg)

            if "email" in input_data:
                validate_email_form(email=input_data.get("email"))

            # TODO - add here password validation as well.

            return func(self, *func_args, **func_kwargs)
        return arguments_wrapper
    return function_wrapper


def validate_email_form(email):
    """
    Valdiates that the email the client provided is indeed a valid email.

    Args:
        email (str): email name.

    Raises:
        EmailNotValidError: in case the email provided is not a valid email.
    """
    try:
        validate_email(email=email)
    except EmailNotValidError:
        raise BadEmailError(email=email)
