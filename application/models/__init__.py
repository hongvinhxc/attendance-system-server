import datetime
import mongoengine as db
from flask_mongoengine import MongoEngine

MongoDB = MongoEngine()

def init_app(app):
    MongoDB.init_app(app)

class BaseDocument(db.DynamicDocument):
    meta = {'abstract': True}
    
    creation_date = db.DateTimeField()
    modified_date = db.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(BaseDocument, self).save(*args, **kwargs)
