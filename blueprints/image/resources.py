from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Images
from sqlalchemy import desc

bp_image = Blueprint('image', __name__)
api = Api(bp_image)