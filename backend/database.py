import sqlite3

from typing import List, Union, Optional

from user import User
from session import Session


class Database:

    def __init__(self) -> None:
        # Generate tables if any do not exist
        self.generate_user_table()
        self.generate_sessions_table()
        self.generate_reviews_table()

# ======================== SQL DB Functions =================================

    def startup_new_connection(self):
        con = sqlite3.connect("./../database/postboxd.db")
        cursor = con.cursor()

        return cursor


    def generate_user_table(self):
        cursor = self.startup_new_connection()
        user_table_cmd = """
            CREATE TABLE IF NOT EXISTS Users (
            username varchar(20) PRIMARY KEY,
            email varchar(40) UNIQUE
            )
        """
        cursor.execute(user_table_cmd)
        cursor.connection.close()

    def generate_sessions_table(self):
        cursor = self.startup_new_connection()
        auth_sesions_cmd = """
            CREATE TABLE IF NOT EXISTS AuthenticatedSessions (
            username varchar(20) REFERENCES Users(username),
            token varchar(40) PRIMARY KEY
            )
        """
        cursor.execute(auth_sesions_cmd)

    def generate_reviews_table(self):
        cursor = self.startup_new_connection()
        reviews_table_cmd = """
            CREATE TABLE IF NOT EXISTS Reviews (
            username varchar(20),
            game_id integer,
            rating integer,
            comment varchar(200),
            PRIMARY KEY(username, game_id),
            FOREIGN KEY (username) REFERENCES Users(username)
            )
        """
        cursor.execute(reviews_table_cmd)



# ======================== User DB Functions =================================

    def register_new_user(self, user: User):
        """Register a new user"""
        cursor = self.startup_new_connection()
        new_usr_cmd = """
            INSERT INTO Users
            VALUES (?, ?)
        """

        cursor.execute(new_usr_cmd, (user.username, user.email))
        cursor.connection.commit()

    def get_user_by_name(self, username: str):
        """Look up a user in the DB by username. Returns None if no user exists"""
        cursor = self.startup_new_connection()
        usr_lookup_cmd = """
        SELECT *
        FROM Users
        WHERE username = ?
        """
        user_data = cursor.execute(usr_lookup_cmd, (username,)).fetchone()
        if user_data is not None:
            # FIXME
            usr = User(user_data[0], "tmp", user_data[1])
            return usr
        else:
            return None

    def get_user_by_email(self, email: str):
        """Look up a user in the DB by username. Returns None if no user exists"""
        cursor = self.startup_new_connection()
        usr_lookup_cmd = """
        SELECT *
        FROM Users
        WHERE email = ?
        """
        user_data = cursor.execute(usr_lookup_cmd, (email,)).fetchone()
        if user_data is not None:
            # FIXME
            usr = User(user_data[0], "tmp", user_data[1])
            return usr
        else:
            return None

    def update_user_object(self, user: User):
        # TODO
        pass

# # ======================== Session DB Functions ============================

    def add_session(self, username: str, usr_token: str):
        """Authenticate a new token for a particular user"""
        cursor = self.startup_new_connection()
        new_session_cmd = """
            INSERT INTO AuthenticatedSessions(username, token)
            VALUES (?, ?)
        """

        cursor.execute(new_session_cmd, (username, usr_token))
        cursor.connection.commit()


# def add_token_entry(user: User, usr_token: str):
#     authenticated_sessions.append(Session(usr_token, user))

# def session_exists(usr_token: str):
#     return next((True for session in authenticated_sessions if
#                  session.usr_token == usr_token), False)

# def lookup_user_token(username: str) -> Optional[str]:
#     # TODO fix nested lookups
#     return next((session.usr_token for session in authenticated_sessions if
#                  session.user.username == username), None)

# def lookup_token_user(usr_token: str) -> Union[User, None]:
#     return next((session.user for session in authenticated_sessions if
#           session.usr_token == usr_token), None)

# def remove_session(usr_token: str):
#     for session in authenticated_sessions:
#         if session.usr_token == usr_token:
#             authenticated_sessions.remove(session)

