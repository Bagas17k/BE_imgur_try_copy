from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Komens
from blueprints.user.model import Users
from datetime import datetime
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
        parser.add_argument('komen', location='json', required=True)
        parser.add_argument('image_id', location='json', required=True)

        args = parser.parse_args()

        claims = get_jwt_claims()
        user_id  = claims['id']
        
        komen = Komens(args['komen'], user_id, args['image_id'])
        komen.created_at = datetime.now()
        db.session.add(komen)
        db.session.commit()

        app.logger.debug('DEBUG: %s', komen)

        return marshal(komen, Komens.response_fields), 200

class KomenListResource(Resource):
    def get(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('komen', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('created_at'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))


        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])

        qry = Komens.query.filter_by(image_id=id)

        if args['komen'] is not None:
            qry = qry.filter_by(komen=args['komen'])
        
        if args['orderby'] is not None:
            if args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Komens.created_at))
                else:
                    qry = qry.order_by(Komens.created_at)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            QRY = marshal(row, Komens.response_fields)
            user = Users.query.filter_by(
                id=QRY['user_id']).first()
            QRY['user'] = marshal(user, Users.response_image)
            rows.append(QRY)

        return rows, 200





api.add_resource(KomenResource, '', '/member')
api.add_resource(KomenListResource, '', '/user/<id>')


