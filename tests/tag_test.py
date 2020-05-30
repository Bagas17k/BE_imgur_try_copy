import json
from io import BytesIO
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestTagCrud():
    def test_tag(self, client, init_database):
        token = create_token()
        res = client.get('/tag/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_not_found_tag(self, client, init_database):
        token = create_token()
        res = client.get('/tag/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_delete_tag(self, client, init_database):
        token = create_token()
        res = client.delete('/tag/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_notfound_tag(self, client, init_database):
        token = create_token()
        res = client.delete('/tag/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_tag_list(self, client, init_database):
        token = create_token()
        res = client.get('/tag',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_tag(self, client, init_database):
        token = create_token()
        with open('/home/alta7/Downloads/politics.jpeg', 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        res = client.post('/tag',
                        content_type='multipart/form-data',
                        headers={'Authorization': 'Bearer ' + token},
                        data={'name':'tes',
                              'img_url':(imgStringIO1, 'img1.jpg')
                            })
        
        res_json = json.loads(res.data)
        assert res.status_code == 200