from flask import request
from api.errors import InvalidInputData


def validate_input_data(*arguments):

    def first_wrapper(func):

        def second_wrapper(self, *func_args, **func_kwargs):

            input_data = request.json

            for arg in arguments:
                if arg not in input_data:
                    raise InvalidInputData(arg=arg)

            return func(self, *func_args, **func_kwargs)
        return second_wrapper
    return first_wrapper
