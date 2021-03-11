import hashlib
import binascii
import os

from api.service.service import UserService
from api.input_valdiation import validate_input_data
from api.database import DatabaseOperations


class UserServiceImplementation(UserService):

    #  TODO - need to implement all the logic of this class, right now it only has DB operations.

    def __init__(self, model=None):
        self._database_operations = DatabaseOperations(model=model)
        self._model = model

    @validate_input_data("email", "username", "password")
    def create(self, **new_user_body_request):
        """
        Creates a new user and inserts it into the DB.

        Keyword Arguments:
            email (str): user email.
            username (str): user name.
            password (str): non-hashed password.
        """
        self._database_operations.insert(**new_user_body_request)
        return new_user_body_request

    def update(self, **update_user_body_request):
        """
        Updates an existing user and updates the DB.

        Keyword Arguments:
            email (str): user email.
            username (str): user name.
            password (str): non-hashed password.
        """
        pass

    def delete(self, username):
        """
        Deletes an existing user and updates the DB.

        Args:
            username (str): user name to delete.
        """
        self._database_operations.delete(primary_key_value=username)
        return ""

    def get_many(self):
        """
        Get all the available users from the DB.
        """
        pass

    def get_one(self, username):
        """
        Get a user by a username.

        Args:
             username (str): user name to get.
        """
        user = self._database_operations.get(primary_key_value=username)
        return {"email": user.email, "password": user.password, "username": user.username}


class User(object):
    def __init__(self):
        return


def hash_password(password, hashname='sha512', num_of_iterations=10000, salt_bytes=60):
    """
    Hashes a password combined with a salt value.

    Args:
        password (str): password to hash.
        hashname (str): which hashing should be performed. e.g.: "sha512", "sha256"
        num_of_iterations (int): the num of iterations that the hash function will operate to encrypt the data.
        salt_bytes (int): number of salt bytes for hashing usage.

    Returns:
        str: hashed password representation.
    """
    salt = hashlib.sha256(os.urandom(salt_bytes)).hexdigest().encode('ascii')

    pwdhash = hashlib.pbkdf2_hmac(
        hash_name=hashname, password=password.encode('utf-8'), salt=salt, iterations=num_of_iterations
    )
    pwdhash = binascii.hexlify(data=pwdhash)

    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password, hashname='sha512', num_of_iterations=10000):
    """
    Checks whether a provided user by the client is indeed the correct password.

    Args:
        stored_password (str): The stored password from the DB.
        provided_password (str): the password that the client provides.
        hashname (str): which hashing should be performed on the provided password. e.g.: "sha512", "sha256"
        num_of_iterations (int): the num of iterations that the hash function will operate to encrypt the provided pass.

    Returns:
        bool: if the provided usr by the client is the same as stored password, False otherwise.
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]

    pwdhash = hashlib.pbkdf2_hmac(
        hash_name=hashname,
        password=provided_password.encode('utf-8'),
        salt=salt.encode('ascii'),
        iterations=num_of_iterations
    )
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')

    return pwdhash == stored_password
