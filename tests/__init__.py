import pytest 
import logging
import json
import hashlib
import uuid
from sqlalchemy.sql import func
from blueprints import app, cache, db
from flask import Flask, request, json
from blueprints.user.model import Users
from blueprints.image.model import Images
from blueprints.komen.model import Komens
from blueprints.tag.model import Tags

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    db.drop_all()
    db.create_all()
    
    salt = uuid.uuid4().hex
    encoded = ('%s%s' %("alta123", salt)).encode('utf-8')
    hashpass = hashlib.sha512(encoded).hexdigest()
    encoded2 = ('%s%s' %("alta123", salt)).encode('utf-8')
    hashpass2 = hashlib.sha512(encoded2).hexdigest()
    user_internal = Users(username='admin', password=hashpass,email='aaa@mail.com',phone='0829718268162', status=True, salt=salt)
    user_noninternal = Users(username='aji', password=hashpass2,email='aaa1@mail.com',phone='082971868162', status=False, salt=salt)    
    db.session.add(user_internal)
    db.session.add(user_noninternal)

    tag = Tags(name='Funny', img_url='facebook.com')
    db.session.add(tag)
    db.session.commit()

    image = Images(img_title='kadal', img_url='facebook.com', deskripsi='aaaa', user_id=1, tag_id=1)
    db.session.add(image)
    db.session.commit()

    komen = Komens(komen='asasa', user_id=1, image_id=1)
    db.session.add(komen)
    db.session.commit()

    
    
    yield db
    
    db.drop_all()
    
    
def create_token():
    token = cache.get('test-token')
    if token is None:
        data={
            'username': 'admin',
            'password': 'alta123'
        }
    
        req = call_client(request)
        res = req.get('/login', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token

def create_token_non_internal():
    token = cache.get('test-token-non-internal')
    if token is None:
        data={
            'username': 'aji',
            'password': 'alta123'
        }
    
        req = call_client(request)
        res = req.get('/login', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-non-internal', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token