from flask import Blueprint
from flask_restful import Api
from CountOccurrences.api.resources import getCountOccurrences

blueprint = Blueprint("api", __name__, url_prefix="/api/v2")
api = Api(blueprint)

api.add_resource(getCountOccurrences, "/count_occurrences/<string:word>", endpoint="count_occurrences")