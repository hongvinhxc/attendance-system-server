from calendar import MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
import mongoengine as db

from application.models import BaseDocument

class NestedWorkingTime(db.EmbeddedDocument):
    morning =  db.ListField(db.StringField(), max_length=2)
    afternoon =  db.ListField(db.StringField(), max_length=2)

class WorkingTime(BaseDocument):
    holidays = db.ListField(db.StringField())
    working_day = db.ListField(db.IntField(), choices=[MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY])
    working_time = db.EmbeddedDocumentField(NestedWorkingTime)