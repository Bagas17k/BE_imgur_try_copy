from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15), unique=True)
    salt = db.Column(db.String(255))
    status = db.Column(db.String(30), nullable=True, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
   

    response_fields ={
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'email':fields.String,
        'phone':fields.String,
        'status' : fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
        }
    
    response_image = {
        'id':fields.Integer,
        'username':fields.String
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'status' : fields.String
    }

    def __init__(self, username, password, email, phone, status, salt):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.status = status
        self.salt = salt
      

    def __repr__(self):
        return '<User %r>'%self.id