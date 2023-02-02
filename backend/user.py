from typing import List
from review import Review


class User():
    """
    Class to represent a postboxd User
    """

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.reviews: List[Review] = []


    def fetchReviewList(self):
        """
        Get all the movies the user has ever rated
        """
        return self.reviews

    def addReview(self, review: Review):
        """
        Add a new review to the User's global list
        """
        if review.get_film() in [review.get_film() for review in self.reviews]:
            print(f"Could not add review to {self.username}'s " +
                  "list: already reviewed")
        self.reviews.append(review)
