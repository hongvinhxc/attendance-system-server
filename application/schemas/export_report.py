from marshmallow import fields, validate

from application.schemas import BaseSchema, PaginationSchema


class GetExportReportListSchema(PaginationSchema):
    pass

    
class ExportReportSchema(BaseSchema):
    month = fields.DateTime(required=True, format="%Y-%m")