from flask_restful import Resource, request
from flask import make_response, jsonify
from api.response import response_decorator
from api.input_valdiation import validate_input_data


class Controller(Resource):

    """
    "Abstract class" for all the controllers in the api to implement rest-api methods.
    """

    def post(self):
        """
        Create a new resource on the server
        """
        pass

    def get(self):
        """
        Get an existing resource from the server
        """
        pass

    def put(self):
        """
        Update an existing resource on the server
        """
        pass

    def delete(self):
        """
        Delete an existing resource from the server
        """
        pass


class UserController(Controller):

    @response_decorator(code=200)
    def post(self):
        """
        Endpoint to create a new user on the server.
        """
        return request.json

    @response_decorator(code=200)
    def get(self):
        """
        Endpoint to get an existing user from the server.
        """
        return {"username": "bla"}

    @response_decorator(code=200)
    def put(self):
        """
        Endpoint to update an existing user in the server.
        """
        return

    @response_decorator(code=204)
    def delete(self):
        """
        Endpoint to delete an existing user from the server.
        """
        return