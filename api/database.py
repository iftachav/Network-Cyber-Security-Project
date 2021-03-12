from api.flask_config import app
from flask_sqlalchemy import SQLAlchemy
from api.errors import (
    ResourceNotFoundError,
    DatabaseInsertionError,
    DatabaseDeletionError
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NetworkSecurityDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserModel(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)


db.create_all()


class DatabaseOperations(object):
    """
    This class is responsible for database operations such as insert, delete, get and update our resources on the api.
    """
    def __init__(self, model=None):
        """
        init the DatabaseOperations object.

        Args:
            model (Model): any class that inherits db.Model. e.g.: UserModel.
        """
        self._model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        """
        a setter for the 'model' attribute.
        """
        self._model = model

    def insert(self, updated_model=None, **kwargs):
        """
        Inserts a new model instance to the DB.

        Args:
            updated_model (Model): any class which inherits from db.Model. e.g.: UserModel

        Raises:
            DatabaseInsertionError: in case insertion error to the DB occurred.
        """
        if updated_model:
            new_model = updated_model
        else:
            new_model = self._model(**kwargs)

        try:
            db.session.add(new_model)
            db.session.commit()
        except Exception as err:
            raise DatabaseInsertionError(error_msg=str(err))

    def update(self, **kwargs):

        found_model = self._model.query.get(kwargs.get("username"))


    def get(self, primary_key_value, resource_type="Username"):
        """
        Returns a model object in case found.

        Args:
             primary_key_value (str): the primary key value of the model.
             resource_type (str): the type of the primary key we search for. e.g.: Username

        Returns:
            Model: any class that inherits db.Model. e.g.: UserModel.

        Raises:
            ResourceNotFoundError: in case resource was not found on the server.
        """
        found_model = self._model.query.get(primary_key_value)
        if found_model:  # in case the found_model is None, it means that we couldn't find that resource.
            return found_model

        raise ResourceNotFoundError(resource=primary_key_value, resource_type=resource_type)

    def delete(self, primary_key_value):
        """
        Deletes a model from the api database.

        Args:
             primary_key_value (str): the primary key value of the model.

        Raises:
            DatabaseDeletionError: in deletion operation was not successful.
        """
        found_model = self.get(primary_key_value=primary_key_value)

        try:
            db.session.delete(found_model)
            db.session.commit()
        except Exception as err:
            raise DatabaseDeletionError(error_msg=str(err))
