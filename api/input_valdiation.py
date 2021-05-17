from flask import request
from email_validator import validate_email, EmailNotValidError

from api.errors import InvalidInputData, BadEmailError, BadPasswordError

from api.password_config import *
import time


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

            if "password" in input_data:
                print(input_data.get("password"))
                validate_password_newUser(input_data.get("password"))
            # TODO - add here password validation as well.

            return func(self, *func_args, **func_kwargs)
        return arguments_wrapper
    return function_wrapper


def validate_email_form(email):
    """
    Validates that the email the client provided is indeed a valid email.

    Args:
        email (str): email name.

    Raises:
        EmailNotValidError: in case the email provided is not a valid email.
    """
    try:
        validate_email(email=email)
    except EmailNotValidError:
        raise BadEmailError(email=email)


def check_requirements(password):
    for k, v in REQUIREMENTS:
        if k == "Upper" and v:
            if not any(c.isupper() for c in password):
                return False
            print("upper ok")
        if k == "Lower" and v:
            if not any(c.islower() for c in password):
                return False
            print("Lower ok")
        if k == "Digits" and v:
            if not any(c.isdigit() for c in password):
                return False
            print("Digits ok")
        if k == "Special" and v:
            if not any(c in SPECIAL_CHARACTERS for c in password):
                return False
            print("Special ok")
    return True


def validate_password_newUser(password):
    if not len(password) >= PASSWORD_LEN:  # At least 10 characters ?
        raise BadPasswordError(password)
    print("length is", len(password))
    if not check_requirements(password):
        raise BadPasswordError(password)
    if search_password(password):
        raise BadPasswordError(password)


def validate_password_updated(user, password):
    validate_password_newUser(password)


def search_password(password):
    # if password is in file - raise BadPasswordError
    return check_if_string_in_file(FILENAME, password)


def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r', errors="ignore") as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False

# search_password("leftout2")
