import mongoengine as db

from application.models import BaseDocument


class ExportReport(BaseDocument):
    filename = db.StringField(required=True)
    report_month = db.DateTimeField(required=True)
