import json
from io import BytesIO
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestImageCrud():
    def test_post_image(self, client, init_database):
        token = create_token()
        with open('/home/alta7/Downloads/politics.jpeg', 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        res = client.post('/image',
                        content_type='multipart/form-data',
                        headers={'Authorization': 'Bearer ' + token},
                        data={'img_title':'tes',
                              'img_url':(imgStringIO1, 'img1.jpg'),
                              'deskripsi':'sasa',
                              'tag_id':1
                            })
        
        res_json = json.loads(res.data)
    
    def test_post_image_str(self, client, init_database):
        token = create_token()
        res = client.post('/image/string',
                        content_type='multipart/form-data',
                        headers={'Authorization': 'Bearer ' + token},
                        data={'img_title':'tes',
                              'img_url':'asasa.com',
                              'deskripsi':'sasa',
                              'tag_id':1
                            })
        
        res_json = json.loads(res.data)
    
    def test_image(self, client, init_database):
        token = create_token()
        res = client.get('/image/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_image_notfound(self, client, init_database):
        token = create_token()
        res = client.get('/image/1000',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_image_list(self, client, init_database):
        token = create_token()
        res = client.get('/image',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_image_list_filter(self, client, init_database):
        token = create_token()
        param = {'img_title':'asaas'}
        res = client.get('/image',query_string=param,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
