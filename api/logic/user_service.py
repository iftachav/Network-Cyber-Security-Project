import hashlib
import binascii
import os

from api.service.service import UserService
from api.input_valdiation import validate_input_data


class UserServiceImplementation(UserService):

    def __init__(self):
        self._database = None

    @validate_input_data("email", "username", "password")
    def create(self, **new_user_body_request):
        """
        Creates a new user and inserts it into the DB.

        Keyword Arguments:
            email (str): user email.
            username (str): user name.
            password (str): non-hashed password.
        """
        pass

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
        pass

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
        pass


class User(object):
    def __init__(self):
        return


def hash_password(password):
    """
    Hashes a password combined with a salt value.

    Args:
        password (str): password to hash.

    Returns:
        str: hashed password representation.
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)

    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """
    Checks whether a provided user by the client is indeed the correct password.

    Args:
        stored_password (str): The stored password from the DB.
        provided_password (str): the password that the client provides.

    Returns:
        bool: if the provided usr by the client is the same as stored password, False otherwise.
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]

    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')

    return pwdhash == stored_password
