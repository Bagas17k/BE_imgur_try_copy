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

class KomenResource(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('komen', location='form', required=True)
        parser.add_argument('image_id', location='form', required=True)

        args = parser.parse_args()

        claims = get_jwt_claims()
        user_id  = claims['id']

        komen = Komens(args['komen'], user_id, args['image_id'])
        db.session.add(komen)
        db.session.commit()

        app.logger.debug('DEBUG: %s', komen)

        return marshal(komen, Komens.response_fields), 200

