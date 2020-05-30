import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestUserCrud():
    def test_user_list_username(self, client, init_database):
        token = create_token()
        param = {'username':'tes'}
        res = client.get('/user',query_string=param,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_list(self, client, init_database):
        token = create_token()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user(self, client, init_database):
        token = create_token()
        res = client.get('/user/member',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    
    def test_post_client(self, client, init_database):
        token = create_token()
        data={
                "username":"bebas aja",
                "password":"sekarepmu"
        }
        res = client.post('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    