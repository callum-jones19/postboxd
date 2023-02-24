"""

"""
from time import sleep

import database as db
from user import User
from auth import AuthHandler
from review import Review

from database import Database
from auth import AuthHandler

def main() -> None:
    # Initialise a blank database
    database = Database()
    auth = AuthHandler(database)

    database.reset_tables()

    print(auth.register_user("callum_jonessad222",
                       "fuck1",
                       "callasdumasd.o.jones@protonmail.com"))
    print(auth.register_user("callum_jones",
                       "fuck123123",
                       "callum.o.jones+2@protonmail.com"))
    print(auth.register_user("callum_jones123",
                       "fuck123123",
                       "callum.o.jones@protonmail.com"))
    print(auth.register_user("callum_jones",
                       "fuck123123",
                       "callum.o.jones+2@protonmail.com"))
    print(auth.register_user("callum_jonessad222das",
                       "fuck1",
                       "callasdumasd.o.jones@protonmail.com"))

    print(auth.login_user("callum_jones", "test_wrong"))
    data = auth.login_user("callum_jones", "fuck123123")
    token = data["token"]

    print(database.get_usr_by_token(token))

    # # Now let's give our user some reviews
    # callum_review_eeaao = Review(545611, 10, "Sometimes nothing is everything")
    # callum.addReview(callum_review_eeaao)

    # # Now let's give our user some reviews
    # callum_review_ann = Review(300668, 9, "Pretty and existential")
    # callum.addReview(callum_review_ann)

    # # Now our user wants to view their existing review
    # callum_reviews = callum.fetchReviewList()
    # print("========== Callum's Reviews ==========")
    # for review in callum_reviews:
    #     review_str = (f"{review.get_game()}: " +
    #                   f"[{review.get_rating()}] {review.get_comment()}")
    #     print(review_str)


if __name__ == "__main__":
    main()
