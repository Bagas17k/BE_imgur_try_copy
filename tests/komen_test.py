import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestKomenCrud():
    def test_post_komen(self, client, init_database):
        token = create_token()
        data={
                "komen":"bebas aja",
                "image_id":1,

        }
        res = client.post('/komen',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_komen_list(self, client, init_database):
        token = create_token()
        res = client.get('/komen/user/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_komen_list_komen(self, client, init_database):
        token = create_token()
        param = {'komen':'tes'}
        res = client.get('/komen/user/1',query_string=param,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_komen_list_order_sort(self, client, init_database):
        token = create_token()
        param = {'orderby':'created_at','sort':'desc'}
        res = client.get('/komen/user/1',query_string=param,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_komen_list_order_sort_ASC(self, client, init_database):
        token = create_token()
        param = {'orderby':'created_at','sort':'asc'}
        res = client.get('/komen/user/1',query_string=param,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

