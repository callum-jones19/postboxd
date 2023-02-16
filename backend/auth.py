import secrets

import database

from user import User


def register_user(username: str, password: str, email: str):
    # Check that the username is not already registered
    if database.find_user_by_name(username) is not None:
        log_msg = ("Attempted to register a username that is already " +
                   "taken. Rejecting request...")
        print(log_msg)
        return {"status": "error", "code": "username_taken"}

    if database.find_user_by_email(email) is not None:
        log_msg = ("Attempted to register an email that is already " +
                   "taken. Rejecting request...")
        print(log_msg)
        return {"status": "error", "code": "email_taken"}

    new_user = User(username, password, email)
    print(f"Registered new user with username {username}")
    database.register_new_user(new_user)

    return {"status": "success"}


def login_user(username: str, password: str):
    """Given a username/pass combo, try to authenticate the given user"""
    target_user = database.find_user_by_name(username)
    if target_user is None:
        return {"status": "error", "code": "user_does_not_exist"}

    if password != target_user.password:
        return {"status": "error", "code": "incorrect_password"}

    if database.lookup_user_token(username) is not None:
        return {"status": "error", "code": "user_already_logged_in"}

    # Generate login token for this user
    token = secrets.token_urlsafe()
    database.add_token_entry(target_user, token)
    return {"status": "success", "token": token}


def logout_user(usr_token: str):
    """Given an authentication token, de-authenticate it"""
    if not database.session_exists(usr_token):
        return {"status": "error", "code": "token_not_authenticated"}

    database.remove_session(usr_token)
    return {"status": "success"}
