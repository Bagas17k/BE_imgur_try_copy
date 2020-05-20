from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Komens
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import werkzeug
import requests

bp_komen = Blueprint('komen', __name__)
api = Api(bp_komen)