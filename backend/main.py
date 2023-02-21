"""

"""
import database as db
from user import User
from auth import AuthHandler
from review import Review

from database import Database

def main():
    # Initialise a blank database
    database = Database()

    # Register our first user
    callum = User("callum_jones", "fuck1", "callum.o.jones@protonmail.com")
    print(database.register_new_user(callum))
    callum = User("callum_jones", "fuck123123", "callum.o.jones+2@protonmail.com")
    print(database.register_new_user(callum))
    callum = User("callum_jones123", "fuck123123", "callum.o.jones@protonmail.com")
    print(database.register_new_user(callum))
    callum = User("callum_jones123", "fuck123123", "callum.o.jones+2@protonmail.com")
    print(database.register_new_user(callum))

    database.get_user_by_name("callum_jones")

    # Now let's give our user some reviews
    callum_review_eeaao = Review(545611, 10, "Sometimes nothing is everything")
    callum.addReview(callum_review_eeaao)

    # Now let's give our user some reviews
    callum_review_ann = Review(300668, 9, "Pretty and existential")
    callum.addReview(callum_review_ann)

    # Now our user wants to view their existing review
    callum_reviews = callum.fetchReviewList()
    print("========== Callum's Reviews ==========")
    for review in callum_reviews:
        review_str = (f"{review.get_game()}: " +
                      f"[{review.get_rating()}] {review.get_comment()}")
        print(review_str)


if __name__ == "__main__":
    main()
