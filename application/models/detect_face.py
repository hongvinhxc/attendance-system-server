import mongoengine as db

from application.models import BaseDocument


class EncodedFace(BaseDocument):
    data = db.ListField()
