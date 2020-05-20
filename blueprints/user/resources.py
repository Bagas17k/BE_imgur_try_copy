from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Users
from sqlalchemy import desc
import uuid
import hashlib

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json')
        parser.add_argument('status', location='json', type=bool)
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        user = Users(args['username'], hash_pass, args['status'], salt)
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG: %s', user)

        return marshal(user, Users.response_fields), 200

    def get(self, id=None):
        qry = Users.query.get(id)

        if qry is not None:
            return marshal(qry, Users.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'id is gone'}, 404, {'Content-Type': 'application/json'}

api.add_resource(UserResource, '', '/<id>')