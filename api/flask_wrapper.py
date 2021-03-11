
from flask_restful import Api
from api.endpoints import UserController
from api.response import HttpMethods
from api.flask_config import app
from api.database import UserModel
from api.logic.user_service import UserServiceImplementation


class FlaskAppWrapper(object):
    """
    This is a class to wrap flask program and to create its endpoints to functions.

    Attributes:
        self._api (FlaskApi) - the api of flask.
    """

    def __init__(self, application):
        self._api = Api(app=application)
        self._app = application
        self.add_endpoints()

    def run(self, host='127.0.0.1', debug=True, threaded=True):
        """
        Run flask app.
        """
        self._app.run(host=host, debug=debug, threaded=threaded)

    def add_endpoints(self):
        """
        Adds all the endpoints to the server
        """
        self._user_endpoints()

    def _user_endpoints(self):
        """
        Adds user endpoints.
        """
        user_controller_kwargs = {"user_model": UserModel, "user_service_implementation": UserServiceImplementation}

        self._api.add_resource(
            UserController,
            '/Register',
            endpoint='/Register',
            methods=[HttpMethods.POST],
            resource_class_kwargs=user_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/Login/<username>',
            endpoint='/Login/<username>',
            methods=[HttpMethods.GET],
            resource_class_kwargs=user_controller_kwargs,
        )

        self._api.add_resource(
            UserController,
            '/ChangePassword',
            endpoint='/ChangePassword',
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


FlaskAppWrapper(application=app).run()
