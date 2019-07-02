from marshmallow import Schema, fields
from datetime import datetime

from web_app.app import db


class User(db.Model):

    def __init__(self, name, username, password, id=None):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text)
    pub_data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    categroy_id = db.Column(db.Integer, db.ForeignKey('categroy.id'),
                            nullable=False)

    categroy = db.relationship('Categroy',
                               backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r> ' % self.title


class Categroy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Catrgroy %r> ' % self.title


class UserSchema(Schema):
    # id = fields.Int()
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()
