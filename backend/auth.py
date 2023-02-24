import secrets
import bcrypt

from database import Database
from user import User


class AuthHandler():
    """
    Class to manage all high-level authentication functions. This takes care
    of actually managing incoming authentication requests, etc, so that the
    DB does not have to worry about
    """

    def __init__(self, database: Database) -> None:
        self.db = database

    def register_user(self, username: str, password_plaintext: str, email: str):
        new_user = User(username, email)

        if self.db.get_user_by_name(username) is not None:
            return {"status": "error", "code": "username_already_registered"}

        if self.db.get_user_by_email(email) is not None:
            return {"status": "error", "code": "email_already_registered"}

        self.db.register_new_user(new_user)

        # Password gen
        (salt, pwd_hashed) = self.encrypt_password(password_plaintext, bcrypt.gensalt())
        self.db.register_new_password(username,
                                      pwd_hashed,
                                      salt)

        return {"status": "success"}


    def encrypt_password(self, plaintext_pwd: str, salt: bytes):
        pwd_encoded = plaintext_pwd.encode()
        pwd_hashed = bcrypt.hashpw(pwd_encoded, salt)
        return (salt.decode(), pwd_hashed.decode())

    def login_user(self, username: str, password: str):
        """Given a username/pass combo, try to authenticate the given user"""
        target_user = self.db.get_user_by_name(username)
        if target_user is None:
            return {"status": "error", "code": "user_does_not_exist"}

        pwd_data = self.db.get_user_password(username)
        (_, hashed_pwd) = self.encrypt_password(password, pwd_data["password_salt"].encode())
        print(hashed_pwd)
        print(pwd_data["password_hash"])
        if hashed_pwd != pwd_data["password_hash"]:
            return {"status": "error", "code": "incorrect_password"}

        if self.db.get_usr_by_token(username) is not None:
            return {"status": "error", "code": "user_already_logged_in"}

        # Generate login token for this user
        token = secrets.token_urlsafe()
        self.db.add_session(username, token)
        return {"status": "success", "token": token}


    def logout_user(self, usr_token: str):
        """Given an authentication token, de-authenticate it"""
        if not self.db.session_exists(usr_token):
            return {"status": "error", "code": "token_not_authenticated"}

        self.db.remove_session(usr_token)
        return {"status": "success"}
