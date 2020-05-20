from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Tags
from sqlalchemy import desc
import werkzeug
import requests

bp_tag = Blueprint('tag', __name__)
api = Api(bp_tag)

class TagsResources(Resource):
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

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='form', required=True)
        parser.add_argument(
            'img_url', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()

        image_tag = args['img_url']

        if image_tag:
            img_link = self.postImage(image_tag)

        tag = Tags(args['name'], img_link)
        db.session.add(tag)
        db.session.commit()

        app.logger.debug('DEBUG: %s', tag)

        return marshal(tag, Tags.response_fields), 200
    
    def get(self, id):
        qry = Tags.query.get(id)

        if qry is not None:
            return marshal(qry, Tags.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

    def delete(self, id):
        qry = Tags.query.get(id)
        if qry is None:
            return {'status': 'Not Found'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': "Deleted"}, 200

class ProductTypeList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = Tags.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Tags.response_fields))

        return rows, 200


api.add_resource(ProductTypeList, '', '/list')
api.add_resource(TagsResources, '', '/<id>')