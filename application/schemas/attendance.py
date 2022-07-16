from marshmallow import fields, validate

from application.schemas import BaseSchema, PaginationSchema


class GetAttendanceListSchema(PaginationSchema):
    month = fields.DateTime(required=True, format="%Y-%m")
    name = fields.String()
    code = fields.String()
    position = fields.String()


class ExportAttendanceSchema(BaseSchema):
    month = fields.DateTime(required=True, format="%Y-%m")
    date_from = fields.String()
    date_to = fields.String()


class GetAttendanceDetailSchema(BaseSchema):
    month = fields.DateTime(required=True, format="%Y-%m")
    date_from = fields.String()
    date_to = fields.String()

    