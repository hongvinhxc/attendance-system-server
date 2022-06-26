import mongoengine as db
from . import BaseDocument

class Auth(BaseDocument):
    _id = db.ObjectIdField()
    username = db.StringField()
    password = db.StringField()
    password_history = db.ListField(db.StringField())

    def save(self, *args, **kwargs):
        if not self.password_history:
            self.password_history = []
        self.password_history.append(self.password)
        return super(Auth, self).save(*args, **kwargs)