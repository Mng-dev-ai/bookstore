"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_HOST = os.getenv("MYSQL_HOST")
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
