from flask import Blueprint, current_app, jsonify,g, request
from flask_restful import Api
from marshmallow import ValidationError
from BookStore.extensions import apispec
from BookStore.api.resources import BookResource,BookList,getCountOccurrences,Search
from BookStore.api.schemas import BookSchema
import time

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(BookResource, "/books/<int:book_id>", endpoint="book_by_id")
api.add_resource(BookList, "/books", endpoint="books")
api.add_resource(Search, "/search", endpoint="search")
api.add_resource(getCountOccurrences, "/count_occurrences/<string:word>", endpoint="count_occurrences")

@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("BookSchema", schema=BookSchema)
    apispec.spec.path(view=BookResource, app=current_app)
    apispec.spec.path(view=BookList, app=current_app)
    apispec.spec.path(view=Search, app=current_app)
    apispec.spec.path(view=getCountOccurrences, app=current_app)

    
@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400


@blueprint.before_request
def before_request():
    g.request_start_time = time.time()

@blueprint.after_request
def after_request(response):
    diff = time.time() - g.request_start_time
    current_app.logger.info(f"Request with path {request.path} took {diff} seconds")
    return response
