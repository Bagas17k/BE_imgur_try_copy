
from flask_cors import CORS, cross_origin
import json
import config
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_script import Manager
from functools import wraps
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()
app = Flask(__name__)
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)
jwt = JWTManager(app)


flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == "Production":
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else:
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, PUT, GET, DELETE', 'Access-Control-Allow-Headers': '*'}


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
                           json.dumps({
                               'method': request.method,
                               'code': response.status,
                               'uri': request.full_path,
                               'request': requestData,
                               'response': json.loads(response.data.decode('utf-8'))
                           })
                           )
    else:
        app.logger.error("REQUEST_LOG\t%s",
                         json.dumps({
                             'method': request.method,
                             'code': response.status,
                             'uri': request.full_path,
                             'request': requestData,
                             'response': json.loads(response.data.decode('utf-8'))
                         }))
    return response

from blueprints.login import bp_login
from blueprints.user.resources import bp_user
from blueprints.image.resources import bp_image
from blueprints.tag.resources import bp_tag
from blueprints.komen.resources import bp_komen

app.register_blueprint(bp_login, url_prefix='/login')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_image, url_prefix='/image')
app.register_blueprint(bp_tag, url_prefix='/tag')
app.register_blueprint(bp_komen, url_prefix='/komen')


db.create_all()