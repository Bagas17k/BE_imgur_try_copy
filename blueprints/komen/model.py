from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Komens (db.Model):
    __tablename__ = "komen"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    komen = db.Column(db.String(255), nullable=True, default='Title Image')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id':fields.Integer,
        'komen':fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'user_id': fields.Integer,
        'image_id': fields.Integer
    }

    def __init__(self, komen, user_id, image_id):
        self.komen = komen
        self.user_id = user_id
        self.image_id = image_id

    def __repr__(self):
        return '<Komen %r>'%self.id