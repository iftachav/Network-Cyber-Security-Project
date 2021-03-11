from flask import Flask
from flask_restful import Api, Resource
from api.endpoints import UserController
from api.response import HttpMethods
from flask_sqlalchemy import SQLAlchemy


class FlaskAppWrapper(object):
    """
    This is a class to wrap flask program and to create its endpoints to functions.

    Attributes:
        self._api (FlaskApi) - the api of flask.
    """
    app = Flask(__name__)

    def __init__(self):
        self._api = Api(app=FlaskAppWrapper.app)
        self.add_endpoints()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NetworkSecurityDB.db'
        self._db = "a"

    def run(self, host='127.0.0.1', debug=True, threaded=True):
        """
        Run flask app.
        """
        self.app.run(host=host, debug=debug, threaded=threaded)

    def add_endpoints(self):
        """
        Adds all the endpoints to the server
        """
        self._user_endpoints()

    def _user_endpoints(self):
        """
        Adds user endpoints.
        """
        # docker_server_controller_kwargs = {'docker_server_implementation': DockerServerServiceImplementation}

        self._api.add_resource(
            UserController,
            '/Register',
            endpoint='/Register',
            methods=[HttpMethods.POST],
            # resource_class_kwargs=docker_server_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/Login',
            endpoint='/Login',
            methods=[HttpMethods.GET],
            # resource_class_kwargs=docker_server_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/ChangePassword',
            endpoint='/ChangePassword',
            methods=[HttpMethods.PUT],
            # resource_class_kwargs=docker_server_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/DeleteUser',
            endpoint='/DeleteUser',
            methods=[HttpMethods.DELETE],
            # resource_class_kwargs=docker_server_controller_kwargs,
        )

FlaskAppWrapper().run()