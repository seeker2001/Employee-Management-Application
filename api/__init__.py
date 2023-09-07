from flask import Blueprint
from flask_restful import Api
from application import db
from application.models import Employee
from api.searchApi import Search

# flask restful api for getting employees based on their name and address
api_blueprint = Blueprint("api", __name__)
_api = Api(api_blueprint)

_api.add_resource(Search, '/searchApi/<string:search_data>')
