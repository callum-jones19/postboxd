"""
Class to handle the API of the server
"""

from flask import Flask

from user import User
from database import Database

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register():
    pass