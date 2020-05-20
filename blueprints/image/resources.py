from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Images
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import werkzeug
import requests

bp_image = Blueprint('image', __name__)
api = Api(bp_image)

class ImagesResource(Resource):
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
        parser.add_argument('deskripsi', location='form', required=True)
        parser.add_argument('tag_id', location='form', required=True)

        args = parser.parse_args()

        image_product = args['img_url']

        if image_product:
            img_link = self.postImage(image_product)

        claims = get_jwt_claims()

        image = Images(args['img_title'], img_link, args['deskripsi'], claims['id'], args['id'])

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
        parser.add_argument('deskripsi', location='form', required=True)
        parser.add_argument('tag_id', location='form', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()

        image = Images(args['img_title'], args['img_url'], args['deskripsi'], claims['id'], args['id'])

        db.session.add(image)
        db.session.commit()
        app.logger.debug('DEBUG: %s', image)

        return marshal(image, Images.response_fields), 200, {'Content-Type': 'application/json'}



api.add_resource(ImagesResource, '', '')
api.add_resource(ImagesStringResource, '/string', '')
