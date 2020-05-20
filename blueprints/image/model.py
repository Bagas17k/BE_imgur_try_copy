
from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Images (db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_title = db.Column(db.String(255), nullable=True, default='Title Image')
    img_url = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    response_fields = {
        'id':fields.Integer,
        'img_title':fields.String,
        'img_url':fields.String,
        'deskripsi':fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'user_id': fields.Integer,
        'tag_id': fields.Integer
    }

    def __init__(self, img_title, img_url, deskripsi, user_id, tag_id):
        self.img_title = img_title
        self.img_url = img_url
        self.deskripsi = deskripsi
        self.user_id = user_id
        self.tag_id = tag_id

    def __repr__(self):
        return '<Image %r>'%self.id
