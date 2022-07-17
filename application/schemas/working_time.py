from calendar import MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
from marshmallow import fields, validate

from application.schemas import BaseSchema


class WorkingTimeSchema(BaseSchema):
    holidays = fields.List(fields.Date(required=True, format="%d-%m"))
    working_day = fields.List(
        fields.Integer(validate=validate.OneOf([MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY])),
        validate=validate.Length(min=1, max=7)
    )
    working_time = fields.Nested({
        "morning": fields.List(fields.Time(format="%H:%M"), validate=validate.Length(equal=2), required=True),
        "afternoon": fields.List(fields.Time(format="%H:%M"), validate=validate.Length(equal=2), required=True)
    })
