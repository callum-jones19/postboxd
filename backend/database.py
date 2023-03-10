import sqlite3

from typing import List, Union, Optional

from user import User
from session import Session


class Database:

    # TODO improve username datatype

    def __init__(self) -> None:
        # Generate tables if any do not exist
        self.generate_user_table()
        self.generate_passwords_table()
        self.generate_sessions_table()
        self.generate_reviews_table()

        # Caches
        """
        These caches exist to allow us to keep our local variables synchronised
        with the database without excessive coupling between all the data
        types. When a cacheable datatype is fetched from the DB, we store
        it here. Every X seconds, everything in the caches are pushed to the
        DB and then the cache is cleared. This allows for low coupling but
        prevents us from using excessive local memory to handle high user
        loads (I wish haha)
        """
        # FIXME - can add the same user multiple times. Not necessarily an
        # immediate problem, but is a waste of resources an should be fixed
        self.users_cache: List[User] = []


# ======================== SQL DB Functions =================================


    def startup_new_connection(self):
        con = sqlite3.connect("./../database/postboxd.db")
        cursor = con.cursor()

        return cursor

    def reset_tables(self):
        cursor = self.startup_new_connection()
        reset_cmd = """
            DROP TABLE Users
        """
        cursor.execute(reset_cmd)

        reset_cmd = """
            DROP TABLE AuthenticatedSessions
        """
        cursor.execute(reset_cmd)

        reset_cmd = """
            DROP TABLE Reviews
        """
        cursor.execute(reset_cmd)

        pwd_cmd = """
            DROP TABLE Passwords
        """
        cursor.execute(pwd_cmd)

        self.generate_user_table()
        self.generate_passwords_table()
        self.generate_reviews_table()
        self.generate_sessions_table()

        cursor.connection.close()

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

    def generate_passwords_table(self):
        cursor = self.startup_new_connection()
        pwd_cmd = """
            CREATE TABLE IF NOT EXISTS Passwords (
                username varchar(20) REFERENCES Users(username),
                password_hash varchar(80) NOT NULL,
                password_salt varchar(20) NOT NULL,
                PRIMARY KEY(username)
            )
        """
        cursor.execute(pwd_cmd)
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

# ===================== Cache Handling Functions ==============================

    def update_from_caches(self):
        for user in self.users_cache:
            # Update all of the users' reviews into the DB
            for review in user.reviews:
                self.create_new_review(user.username, review.game_id,
                                       review.rating, review.comment)

            # Now update the email
            self.update_user(user)

        # And now remove from the Cache
        self.users_cache.clear()


# ======================== Review DB Functions =================================

    def create_new_review(self, username: str, game_id: int, rating: int,
                          comment: str):
        """Register a new review in the database"""
        cursor = self.startup_new_connection()
        try_update_review = """
            UPDATE Reviews
            SET rating=?, comment=?
            WHERE username=? AND game_id=?
        """
        cursor.execute(try_update_review, (rating, comment, username, game_id))

        try_insert_review = """
            INSERT OR IGNORE INTO Reviews
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(try_insert_review, (username, game_id, rating, comment))
        cursor.connection.commit()
        cursor.connection.close()

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
        cursor.connection.close()
        self.users_cache.append(user)

    def update_user(self, user: User):
        """
        Update an existing user and their reviews in the DB.

        NB: A username is the unique identifier for a user. Python doesn't
        let us enforce that username is STATIC locally (thank you Python),
        but it should be considered such.
        """
        cursor = self.startup_new_connection()
        update_usr_cmd = """
            UPDATE Users
            SET email=?
            WHERE username=?
        """
        cursor.execute(update_usr_cmd, (user.email, user.username))
        cursor.connection.commit()
        cursor.connection.close()

    def register_new_password(self, username: str, password_hashed: str,
                              password_salt: str):
        """Record authentication data to the password table"""
        cursor = self.startup_new_connection()
        new_pwd_cmd = """
            INSERT INTO Passwords
            VALUES (?, ?, ?)
        """
        cursor.execute(new_pwd_cmd, (username, password_hashed, password_salt))
        cursor.connection.commit()
        cursor.connection.close()

    def get_user_password(self, username: str):
        """Get the salt and hash of a user password"""
        cursor = self.startup_new_connection()
        get_pwd_cmd = """
            SELECT password_hash, password_salt
            FROM Passwords
            WHERE username = ?
        """
        password_data = cursor.execute(get_pwd_cmd, (username,)).fetchone()
        cursor.connection.close()
        if password_data is None:
            return None
        else:
            return {"password_hash": password_data[0],
                    "password_salt": password_data[1]}

    def get_user_by_name(self, username: str):
        """Look up a user in the DB by username.
        Returns None if no user exists
        """
        # Always take the cached version, if it exists
        cached_usr = next((user for user in self.users_cache if user.username
                           == username), None)
        print("USR CACHE: " + str(self.users_cache))
        if cached_usr is not None:
            return cached_usr

        cursor = self.startup_new_connection()
        usr_lookup_cmd = """
        SELECT *
        FROM Users
        WHERE username = ?
        """
        user_data = cursor.execute(usr_lookup_cmd, (username,)).fetchone()
        review_lookup_cmd = """
        SELECT *
        FROM Reviews
        WHERE username = ?
        """
        review_data = cursor.execute(review_lookup_cmd, (username,)).fetchall()
        print("REVIEWS: " + str(review_data))

        cursor.connection.close()
        if user_data is not None:
            usr = User(user_data[0], user_data[1])
            for review in review_data:
                usr.addReview(review[1], review[2], review[3])
            self.users_cache.append(usr)
            return usr
        else:
            return None


# # ======================== Session DB Functions ============================

    # FIXME optimise with JOIN statements, instead of making
    # multiple queries to multiple tables.

    def add_session(self, username: str, usr_token: str):
        """Authenticate a new token for a particular user"""
        cursor = self.startup_new_connection()
        new_session_cmd = """
            INSERT INTO AuthenticatedSessions(username, token)
            VALUES (?, ?)
        """

        cursor.execute(new_session_cmd, (username, usr_token,))
        cursor.connection.commit()
        cursor.connection.close()

    def get_usr_by_token(self, token: str):
        """Given a token, look up to see if a user has an authenticated session
        for that
        """
        cursor = self.startup_new_connection()
        get_usr_cmd = """
            SELECT *
            FROM AuthenticatedSessions
            WHERE token = ?
        """
        session_data = cursor.execute(get_usr_cmd, (token, )).fetchone()
        if session_data is None:
            cursor.connection.close()
            return None
        else:
            username = session_data[0]
            user = self.get_user_by_name(username)
            cursor.connection.close()
            return user


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

