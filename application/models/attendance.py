import mongoengine as db

from application.models import BaseDocument


class Attendance(BaseDocument):
    profile_id = db.ObjectIdField(required=True)
    attendance_times = db.ListField(db.DateTimeField())
