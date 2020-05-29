from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import json
from blueprints import db, app
from .model import Users
from sqlalchemy import desc
import uuid
import hashlib

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserResource(Resource):

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.get(claims['id'])
        if qry is not None:
            return marshal(qry, Users.response_fields),200
        return {{'status': 'NOT_FOUND'}, 404}


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('phone', location='json')
        parser.add_argument('status', location='json', type=bool)
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        user = Users(args['username'], hash_pass, args['email'], args['phone'], args['status'], salt)
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG: %s', user)

        return marshal(user, Users.response_fields), 200

    
class UserList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('username', location='args')

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Users.query

        if args['username'] is not None:
            qry = qry.filter_by(status=args['username'])

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200

api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, '', '/member')