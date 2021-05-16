import os

from flask_restful import Api
from api.endpoints import UserController, ClientController
from api.response import HttpMethods
from api.flask_config import app
from api.database import UserModel, ClientModel
from api.logic.user_service import UserServiceImplementation
from api.logic.client_service import ClientServiceImplementation


class FlaskAppWrapper(object):
    """
    This is a class to wrap flask program and to create its endpoints to functions.

    Attributes:
        self._api (FlaskApi): the api of flask object.
        self._app (FlaskApplication): the flask application object.
    """

    def __init__(self, application):
        self._api = Api(app=application)
        self._app = application
        self.add_endpoints()

    def run(self, host='127.0.0.1', debug=True, threaded=True):
        """
        Run flask app.
        """
        self._app.run(
            host=host,
            debug=debug,
            threaded=threaded
        #     ,ssl_context=(os.environ.get("cert.pem"), os.environ.get("key.pem"))
        )

    def add_endpoints(self):
        """
        Adds all the endpoints to the server
        """
        self._user_endpoints()
        self._client_endpoints()

    def _user_endpoints(self):
        """
        Adds user endpoints.
        """
        user_controller_kwargs = {"user_model": UserModel, "user_service_implementation": UserServiceImplementation}

        # self._api.add_resource(
        #     UserController,
        #     '/Logout',
        #     endpoint='/Logout',
        #     methods=[HttpMethods.GET],
        #     resource_class_kwargs=user_controller_kwargs,
        # )

        self._api.add_resource(
            UserController,
            '/Register',
            endpoint='/Register',
            methods=[HttpMethods.POST],
            resource_class_kwargs=user_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/CheckSession',
            endpoint='/CheckSession',
            methods=[HttpMethods.POST],
            resource_class_kwargs=user_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/Login/<username>/<password>',
            endpoint='/Login/<username>/<password>',
            methods=[HttpMethods.GET],
            resource_class_kwargs=user_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/ChangePassword/<username>',
            endpoint='/ChangePassword/username>',
            methods=[HttpMethods.PUT],
            resource_class_kwargs=user_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/DeleteUser/<username>',
            endpoint='/DeleteUser/<username>',
            methods=[HttpMethods.DELETE],
            resource_class_kwargs=user_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/GetAllUsers',
            endpoint='/GetAllUsers',
            methods=[HttpMethods.GET],
            resource_class_kwargs=user_controller_kwargs,
        )

    def _client_endpoints(self):
        """
        Adds client endpoints.
        """
        client_controller_kwargs = {
            "client_model": ClientModel, "client_service_implementation": ClientServiceImplementation
        }
        self._api.add_resource(
            ClientController,
            '/Client',
            endpoint='/Client',
            methods=[HttpMethods.POST],
            resource_class_kwargs=client_controller_kwargs,
        )

        self._api.add_resource(
            ClientController,
            '/Client/<id>',
            endpoint='/Client/<id>',
            methods=[HttpMethods.GET],
            resource_class_kwargs=client_controller_kwargs,
        )

        self._api.add_resource(
            ClientController,
            '/Clients',
            endpoint='/Clients',
            methods=[HttpMethods.GET],
            resource_class_kwargs=client_controller_kwargs,
        )


flask = FlaskAppWrapper(application=app)

# flask.run() should only be used for local host.
# flask.run()
if __name__ == "__main__":
    flask.run()

