from user import User

class Session():
    def __init__(self, usr_token: str, user: User) -> None:
        self.usr_token: str = usr_token
        self.user: User = user
