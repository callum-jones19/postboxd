from typing import List
from review import Review
from game_db import game_exists

class User():
    """
    Class to represent a postboxd User
    """

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.reviews: List[Review] = []

    def fetchReviewsAsDict(self) -> List[dict]:
        """
        Get all the movies the user has ever rated as a dictionary
        """
        return [review.get_review_as_dict() for review in self.reviews]

    def addReview(self, game_id: int, rating: int, comment: str):
        """
        Add a new review to the User's global list
        """
        # Check the user hasn't already reviewed this game
        game_already_reviewed = next((True for existing_review in self.reviews if game_id == existing_review.get_game_id()), False)
        if game_already_reviewed:
            return {"status": "error", "code": "game_already_reviewed"}

        if not game_exists(game_id):
            return {"status": "error", "code": "invalid_game_id"}

        review: Review = Review(game_id, rating, comment)
        self.reviews.append(review)

        return {"status": "success"}
