"""
DO NOT HARD CODE YOUR PRODUCTION URLS. Use creds.ini or use environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# more configuration options here http://flask.pocoo.org/docs/1.0/config/
class Config:
    """
    Base Configuration
    """

    # CHANGE SECRET_KEY!! Use sha256 to generate one and set this as an environment variable
    SECRET_KEY = "testkey"
    DATABASE_URI = os.environ.get("DATABASE_URL")
    DATABASE_USER = os.environ.get("NEO_USER")
    DATABASE_PASS = os.environ.get("NEO_PASSWORD")


class DevelopmentConfig(Config):
    """
    Development Configuration - default config
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production Configuration

    Requires the environment variable `FLASK_ENV=prod`
    """
    DEBUG = False


config = {"dev": DevelopmentConfig, "prod": ProductionConfig}
