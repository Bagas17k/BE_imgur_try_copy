from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Images
from blueprints.user.model import Users
from blueprints.tag.model import Tags
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import werkzeug
import requests

bp_image = Blueprint('image', __name__)
api = Api(bp_image)

class ImagesResource(Resource):

    def get(self, id):
        qry = Images.query.get(id)
        QRY = marshal(qry, Images.response_fields)
        user = Users.query.filter_by(id=QRY['user_id']).first()
        tag = Tags.query.filter_by(id=QRY['tag_id']).first()
        QRY['user'] = marshal(user, Users.response_image)
        QRY['tag'] = marshal(tag, Tags.response_fields)
        if qry is not None:
            return QRY, 200
        return {'status':'Not found'}, 404

    def __init__(self):
        pass
    
    def postImage(self, imgFile):
        url = app.config['IMG_URL']
        clientID = app.config['IMG_CLIENT_ID']

        payload = {}
        files = [('image', imgFile)]
        ncid = 'Client-ID ' + clientID
        headers = {
            'Authorization': ncid
        }

        res = requests.post(url, headers=headers, data=payload, files=files)
        response = res.json()
        print('=====', response)

        link = response['data']['link']
        return link

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('img_title', location='form', required=True)
        parser.add_argument(
            'img_url', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('deskripsi', location='form')
        parser.add_argument('tag_id', location='form', required=True)

        args = parser.parse_args()

        image_product = args['img_url']

        if image_product:
            img_link = self.postImage(image_product)

        claims = get_jwt_claims()

        image = Images(args['img_title'], img_link, args['deskripsi'], claims['id'], args['tag_id'])

        db.session.add(image)
        db.session.commit()
        app.logger.debug('DEBUG: %s', image)

        return marshal(image, Images.response_fields), 200, {'Content-Type': 'application/json'}

class ImagesStringResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('img_title', location='form', required=True)
        parser.add_argument('img_url', location='form', required=True)
        parser.add_argument('deskripsi', location='form')
        parser.add_argument('tag_id', location='form', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()

        image = Images(args['img_title'], args['img_url'], args['deskripsi'], claims['id'], args['tag_id'])

        db.session.add(image)
        db.session.commit()
        app.logger.debug('DEBUG: %s', image)

        return marshal(image, Images.response_fields), 200, {'Content-Type': 'application/json'}

class ImageList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('img_title', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('created_at'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Images.query

        if args['img_title'] is not None:
            qry = qry.filter_by(img_title=args['img_title'])
        
        if args['orderby'] is not None:
            if args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Images.created_at))
                else:
                    qry = qry.order_by(Images.created_at)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            QRY = marshal(row, Images.response_fields)
            tag = Tags.query.filter_by(id=QRY['tag_id']).first()
            QRY['tags'] = marshal(tag, Tags.response_fields)
            rows.append(QRY)

        return rows, 200



api.add_resource(ImageList, '', '/list')
api.add_resource(ImagesResource, '', '/<id>')
api.add_resource(ImagesStringResource, '/string', '')
