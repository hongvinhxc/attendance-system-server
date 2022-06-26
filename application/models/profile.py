import mongoengine as db


class Profile(db.DynamicDocument):
    _id = db.ObjectIdField()
    name = db.StringField()