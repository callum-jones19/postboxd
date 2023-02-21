import secrets

from database import Database
from user import User

class AuthHandler():

    def __init__(self, database: Database) -> None:
        self.db = database


    def register_user(self, username: str, password: str, email: str):
        new_user = User(username, password, email)

        if self.db.get_user_by_name(username) is not None:
            return {"status": "error", "code": "username_already_registered"}

        if self.db.get_user_by_email(email) is not None:
            return {"status": "error", "code": "email_already_registered"}

        self.db.register_new_user(new_user)

        return {"status": "success"}


    def login_user(self, username: str, password: str):
        """Given a username/pass combo, try to authenticate the given user"""
        target_user = self.db.get_user_by_name(username)
        if target_user is None:
            return {"status": "error", "code": "user_does_not_exist"}

        if password != target_user.password:
            return {"status": "error", "code": "incorrect_password"}

        if self.db.lookup_user_token(username) is not None:
            return {"status": "error", "code": "user_already_logged_in"}

        # Generate login token for this user
        token = secrets.token_urlsafe()
        self.db.add_token_entry(target_user, token)
        return {"status": "success", "token": token}


    def logout_user(self, usr_token: str):
        """Given an authentication token, de-authenticate it"""
        if not self.db.session_exists(usr_token):
            return {"status": "error", "code": "token_not_authenticated"}

        self.db.remove_session(usr_token)
        return {"status": "success"}
