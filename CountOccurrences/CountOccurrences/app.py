from flask import Flask
from CountOccurrences import api

def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("CountOccurrences")
    app.config.from_object("CountOccurrences.config")
    if testing is True:
        app.config["TESTING"] = True
    register_blueprints(app)
    return app


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(api.views.blueprint)

