import sqlite3

from typing import List, Union, Optional

from user import User
from session import Session


class Database:

    def __init__(self) -> None:
        self.con = sqlite3.connect("postboxd.db")
        self.cursor = self.con.cursor()
        # Initialise tables
        # TODO if DB does not exist
        # user_table_cmd = """
        #              CREATE TABLE Users (
        #                 username varchar(20) PRIMARY KEY,
        #                 email varchar(40) UNIQUE
        #              )
        #              """

        # review_table_cmd = """
        #              CREATE TABLE AuthenticatedSessions (
        #                 username varchar(20) REFERENCES Users(username),
        #                 token varchar(40) PRIMARY KEY
        #              )
        #              """
        # cursor.execute(user_table_cmd)
        # cursor.execute(review_table_cmd)

# ======================== User DB Functions =================================

    def register_new_user(self, user: User):
        """Register a new user"""


    def find_user_by_name(username: str):
        """Look up a user in the DB by username. Returns None if no user exists"""
        return next((user for user in users_db
                        if user.username == username), None)

    def find_user_by_email(email: str):
        """Look up a user in the DB by email. Returns None if no user exists"""
        return next((user for user in users_db
                        if user.email == email), None)


# ======================== Session DB Functions ============================

def add_token_entry(user: User, usr_token: str):
    authenticated_sessions.append(Session(usr_token, user))

def session_exists(usr_token: str):
    return next((True for session in authenticated_sessions if
                 session.usr_token == usr_token), False)

def lookup_user_token(username: str) -> Optional[str]:
    # TODO fix nested lookups
    return next((session.usr_token for session in authenticated_sessions if
                 session.user.username == username), None)

def lookup_token_user(usr_token: str) -> Union[User, None]:
    return next((session.user for session in authenticated_sessions if
          session.usr_token == usr_token), None)

def remove_session(usr_token: str):
    for session in authenticated_sessions:
        if session.usr_token == usr_token:
            authenticated_sessions.remove(session)

