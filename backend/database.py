from typing import List

from user import User

class Database():
    def __init__(self):
        self.users_db: List[User] = []

    def register_user(self, user: User):
        # Check that the username is not already registered
        if user.username in [user.username for user in self.users_db]:
            log_msg = ("Attempted to register a username that is already " +
                       "taken. Rejecting request...")
            print(log_msg)
            return

        if user.email in [user.email for user in self.users_db]:
            log_msg = ("Attempted to register an email that is already " +
                       "taken. Rejecting request...")
            print(log_msg)
            return


        print(f"Registered new user with username {user.username}")
        self.users_db.append(user)
