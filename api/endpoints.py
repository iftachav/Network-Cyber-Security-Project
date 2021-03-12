from flask_restful import Resource, request
from api.response import response_decorator, HttpCodes
from api.service.service import *


class Controller(Resource):

    """
    "Abstract class" for all the controllers in the api to implement rest-api methods.
    """

    def post(self, *args, **kwargs):
        """
        Create a new resource on the server
        """
        pass

    def get(self, *args, **kwargs):
        """
        Get an existing resource from the server
        """
        pass

    def put(self, *args, **kwargs):
        """
        Update an existing resource on the server
        """
        pass

    def delete(self, *args, **kwargs):
        """
        Delete an existing resource from the server
        """
        pass


class UserController(Controller):
    """
    User controller to interact with the client requests.
    """
    def __init__(self, user_service_implementation, user_model):
        """
        Init the controller class

        Args:
            user_service_implementation (UserServiceImplementation): a class that implements the user service.
            user_model (UserModel): a user model to interact with DB operations.
        """
        self._user_service_implementation = user_service_implementation
        self._user_model = user_model

    @response_decorator(code=HttpCodes.OK)
    def post(self):
        """
        Endpoint to create a new user on the server.

        Returns:
            dict: a new user response to the client.
        """
        return ServiceClassWrapper(
            class_type=self._user_service_implementation,
            model=self._user_model
        ).create(**request.json)

    @response_decorator(code=HttpCodes.OK)
    def get(self, username=None, password=None):
        """
        Endpoint to get an existing user from the server.

        Args:
            username (str): a user name from the URL.
            password (str): a user password from the URL.

        Returns:
            dict/list[dict]: Returns either all users or a single user.
        """
        if username:  # get single user
            return ServiceClassWrapper(
                class_type=self._user_service_implementation,
                model=self._user_model
            ).get_one(username=username, password=password)
        else:  # get all users
            return ServiceClassWrapper(
                class_type=self._user_service_implementation,
                model=self._user_model
            ).get_many()

    @response_decorator(code=HttpCodes.NO_CONTENT)
    def put(self, username):
        """
        Endpoint to update an existing user in the server.
        """
        return ServiceClassWrapper(
            class_type=self._user_service_implementation, model=self._user_model
        ).update(username=username, **request.json)

    @response_decorator(code=HttpCodes.NO_CONTENT)
    def delete(self, username):
        """
        Endpoint to delete an existing user from the server.

        Args:
            username (str): a user name provided from the URL.

        Returns:
            str: should return an empty string as part of the convention of rest APIs.
        """
        return ServiceClassWrapper(
            class_type=self._user_service_implementation,
            model=self._user_model
        ).delete(username=username)
