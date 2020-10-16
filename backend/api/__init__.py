import os

from flask import Flask, request
from flask_cors import CORS

from api.config import config
from api.core import all_exception_handler


# why we use application factories http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app():
    """
    The flask application factory.
    """
    app = Flask(__name__)

    CORS(app)  # add CORS

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    app.config.from_object(config[env])  # config dict is from api/config.py

    # initialize Neo4j 
    from api.models.base import db
    db.init_app(app, config[env].DATABASE_URI, config[env].DATABASE_USER, config[env].DATABASE_PASS)

    # import and register blueprints
    from api.views import main
    app.register_blueprint(main.main)
    app.register_error_handler(Exception, all_exception_handler)

    return app
