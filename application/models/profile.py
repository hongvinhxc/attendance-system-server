import mongoengine as db

from application.models import BaseDocument


class Profile(BaseDocument):
    name = db.StringField(min_length=1, max_length=50, required=True)
    position = db.StringField(min_length=1, max_length=200, required=True)
    code = db.StringField(min_length=1, max_length=10, required=True, unique=True)
    trained = db.BooleanField(default=False)

    def update(self, *args, **kwargs):
        self.trained = False
        return super(Profile, self).update(*args, **kwargs)