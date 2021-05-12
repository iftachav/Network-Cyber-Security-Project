import hashlib
import binascii
import os

from flask import request
from datetime import datetime

from api.service.service import UserService
from api.input_valdiation import validate_input_data
from api.database import DatabaseOperations
from api.errors import InvalidPasswordProvided, UserIsLockedError

from api.password_config import *


class UserServiceImplementation(UserService):

    #  TODO - need to implement all the logic of this class, right now it mostly has DB operations.

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
        # print("user service:create", new_user_body_request)
        new_user_body_request["password"] = hash_password(password=new_user_body_request.get("password"))
        new_user_body_request["history"] = ""
        new_user_body_request["last_try"] = datetime.now()
        new_user_body_request["try_count"] = 0
        new_user_body_request["is_active"] = True
        # print("user service:create", new_user_body_request)
        self._database_operations.insert(**new_user_body_request)
        # print("user service:create", new_user_body_request)
        return new_user_body_request    # maybe it's better to return something else and not the password.

    @validate_input_data("email", "password", create=False)
    def update(self, username, **update_user_body_request):
        """
        Updates an existing user and updates the DB.

        Args:
            username (str): user name.

        Keyword Arguments:
            email (str): user email.
            password (str): non-hashed password.

        Returns:
            str: empty string in case of success.
        """
        user_to_update = self._database_operations.get(primary_key_value=username)
        print("update, user_to_update:", user_to_update)
        if "old_password" in update_user_body_request and verify_password(user_to_update.password, update_user_body_request.get("old_password")):
            if "email" in update_user_body_request:
                user_to_update.email = update_user_body_request.get("email")
            if "password" in update_user_body_request:
                print("update, old p:", user_to_update.password)
                p = update_user_body_request.get("password")
                # hashed_pass = hash_password(password=update_user_body_request.get("password"))
                if not check_in_history(user_to_update.history, p) and not verify_password(user_to_update.password, p):
                    print("update, user_to_update:", user_to_update)
                    user_to_update.history = change_history(user_to_update.history, user_to_update.password)
                    user_to_update.password = hash_password(password=update_user_body_request.get("password"))
                    print("update, new p:", user_to_update.password)
                else:
                    print("update failed")
                    raise InvalidPasswordProvided()
        else:
            print("update failed")
            raise InvalidPasswordProvided()

        self._database_operations.insert(updated_model=user_to_update)

        return ''

    def delete(self, username):
        """
        Deletes an existing user and updates the DB.

        Args:
            username (str): user name to delete.

        Returns:
            str: empty string in case of success.
        """
        self._database_operations.delete(primary_key_value=username)
        return ''

    def get_many(self):
        """
        Get all the available users from the DB.

        Returns:
            list[dict]: a list of all users responses from the DB.
        """
        response = []

        all_users = self._database_operations.get_all()
        for user in all_users:
            response.append({"email": user.email, "password": user.password, "username": user.username})

        return response

    def get_one(self, username, password):
        """
        Get a user by a username & password from the DB..

        Args:
             username (str): user name to get.
             password (str): user password to verify.
        """
        # ip_addr = request.remote_addr

        # attempt = LoginAttemptsServiceImplementation(LoginAttemptsModel()).get_one(username, request.remote_addr)
        # if attempt["num_attempts"] > LOGIN_ATTEMPTS:
        #     raise UserIsLockedError(ip_addr)
        user = self._database_operations.get(primary_key_value=username)
        if (datetime.now() - user.last_try).seconds > LOGIN_LOCK:
            user.is_active = True
            user.try_count = 0
        if user.try_count >= LOGIN_ATTEMPTS:
            user.is_active = False
        if user.is_active:
            if not verify_password(stored_password=user.password, provided_password=password):
                user.try_count += 1
                user.last_try = datetime.now()
                self._database_operations.insert(updated_model=user)
                raise InvalidPasswordProvided()
            user.try_count = 0
            self._database_operations.insert(updated_model=user)
            # maybe it's better to return something else and not the password.
            return {"email": user.email, "password": user.password, "username": user.username}
        else:
            self._database_operations.insert(updated_model=user)
            raise InvalidPasswordProvided() # need to throw locked exception


class User(object):

    def __init__(self, username, password, email):
        self._username = username
        self._password = password
        self._email = email

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def email(self):
        return self._email


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
    pwdhash = binascii.hexlify(pwdhash)

    return (salt + pwdhash).decode('ascii')


def check_in_history(history, provided_password):
    history_list = history.split(',')
    for p in history_list:
        if verify_password(p, provided_password):
            return True
    return False


def change_history(history, password):
    history_list = history.split(',')
    if len(history_list) >= HISTORY:
        history_list.pop(0)
    history_list.append(password)
    for p in history_list:
        print(p)
    return ','.join(history_list)



def verify_password(stored_password, provided_password, hashname='sha512', num_of_iterations=10000):
    """
    Checks whether a provided user by the client is indeed the correct password.

    Args:
        stored_password (str): The stored password from the DB.
        provided_password (str): the password that the client provides.
        hashname (str): which hashing should be performed on the provided password. e.g.: "sha512", "sha256"
        num_of_iterations (int): the num of iterations that the hash function will operate to encrypt the provided pass.

    Returns:
        bool: if the provided password by the client is the same as stored password, False otherwise.
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
