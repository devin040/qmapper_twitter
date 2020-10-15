from flask import Blueprint, request
from api.core import create_response

main = Blueprint("main", __name__)


# function that is called when you visit /
@main.route("/")
def index():
    # you are now in the current application context with the main.route decorator
    return create_response(message="test message", data={"testdata": 1})
