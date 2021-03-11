from flask import request
from api.errors import InvalidInputData


def validate_input_data(*arguments):
    """
    Validates that the provided arguments are indeed a part of the json body request.

    Note: in case all the arguments are valid, this decorator just executes the decorated function.

    Args:
        arguments (list[str]): all the keys that should be in the json request.
    """
    def function_wrapper(func):

        def arguments_wrapper(self, *func_args, **func_kwargs):

            input_data = request.json

            for arg in arguments:
                if arg not in input_data:
                    raise InvalidInputData(arg=arg)

            return func(self, *func_args, **func_kwargs)
        return arguments_wrapper
    return function_wrapper
