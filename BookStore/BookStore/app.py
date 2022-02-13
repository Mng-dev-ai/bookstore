from flask import Flask
from BookStore import api
from BookStore.extensions import apispec
from BookStore.extensions import db
from BookStore.extensions import jwt
from BookStore.extensions import migrate
from BookStore import manage
import logging
import sys


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("BookStore")
    app.config.from_object("BookStore.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    configure_logger(app)
    configure_cli(app)
    return app
    

def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)

        
def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(api.views.blueprint)

