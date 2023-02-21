"""
Class to handle the API of the server
"""

from typing import Dict, Optional
from flask import Flask, request

from auth import AuthHandler
from database import Database

from user import User


app = Flask(__name__)
db = Database()
auth_manager = AuthHandler(db)


@app.route("/auth/register", methods=["POST"])
def register() -> Dict:
    register_details: Optional[dict] = request.json
    if register_details is None:
        return {"error": "pray"}

    if "username" not in register_details:
        return {"error": "missing_username_field"}
    if "password" not in register_details:
        return {"error": "missing_password_field"}
    if "email" not in register_details:
        return {"error": "missing_email_field"}

    auth_res = auth_manager.register_user(register_details["username"],
                       register_details["password"], register_details["email"])

    return auth_res

@app.route("/auth/login", methods=["POST"])
def login() -> Dict:
    login_details: Optional[dict] = request.json
    if login_details is None:
        return {"error": "pray"}

    if "username" not in login_details:
        return {"error": "missing_username_field"}

    if "password" not in login_details:
        return {"error": "missing_pwd_field"}

    login_res = auth_manager.login_user(login_details["username"], login_details["password"])
    return login_res

@app.route("/auth/logout", methods=["POST"])
def logout() -> Dict:
    logout_details: Optional[dict] = request.json
    if logout_details is None:
        return {"error": "pray"}

    if "token" not in logout_details:
        return {"error": "missing_token"}

    logout_res = auth_manager.logout_user(logout_details["token"])
    return logout_res

@app.route("/user/<username>/get_reviews")
def get_reviews(username: str) -> Dict:
    target_usr = database.find_user_by_name(username)
    if target_usr is None:
        return {"error": "user_does_not_exist"}

    reviews = target_usr.fetchReviewsAsDict()
    return {"user": username, "reviews": reviews}


@app.route("/user/add_review", methods=["POST"])
def add_review():
    add_review_details: Optional[dict] = request.json
    if add_review_details is None:
        return {"error": "pray"}, 400

    if "token" not in add_review_details:
        return {"status": "error", "code": "missing_token"}, 400

    if "game_id" not in add_review_details:
        return {"status": "error", "code": "missing_game_id"}, 400

    if "rating" not in add_review_details:
        return {"status": "error", "code": "missing_rating"}, 400

    if "comment" not in add_review_details:
        return {"status": "error", "code": "missing_comment"}, 400

    user: Optional[User] = database.lookup_token_user(add_review_details["token"])
    if user is None:
        return {"status": "error", "code": "invalid_token"}, 400

    response = user.addReview(add_review_details["game_id"],
                              add_review_details["rating"],
                              add_review_details["comment"])

    if response["status"] == "error":
        return response, 400
    else:
        return response

