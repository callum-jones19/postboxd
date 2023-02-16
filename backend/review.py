class Review():
    def __init__(self, game_name: int, rating: int, comment: str):
        self.game_id = game_name
        self.rating = rating
        self.comment = comment

    def get_rating(self) -> int:
        return self.rating

    def get_game_id(self) -> int:
        return self.game_id

    def get_comment(self) -> str:
        return self.comment

    def get_review_as_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "rating": self.rating,
            "comment": self.comment
        }
