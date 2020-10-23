from flask import Blueprint, request
from api.core import create_response, serialize_list
from api.models import db

main = Blueprint("main", __name__)


# function that is called when you visit /
@main.route("/")
def index():
    # you are now in the current application context with the main.route decorator
    return create_response(message="test message", data={"testdata": 1})


@main.route("/data")
def data():
    with db.get_db().session() as session:
        result = session.run("MATCH (n) RETURN n")
        return create_response(data={"data": result.data()})


@main.route("/topusers")
def top_users():
    with db.get_db().session() as session:
        result = session.run("""
            MATCH (a:Author) 
            WHERE a.username IS NOT NULL 
            RETURN a.username, a.follower_count 
            ORDER BY a.follower_count DESC
        """)
        return create_response(data={"data": result.data()})


@main.route("/metrics")
def metrics():
    pass
