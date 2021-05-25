
from datetime import datetime

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField


class User(Document):
    name = StringField(max_length=120, unique=True, required=True)
    document = StringField(max_length=120, unique=True, required=True)
    address = StringField(max_length=120, null=True)
    created_date = DateTimeField(default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username