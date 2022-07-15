from marshmallow import fields, validate

from application.schemas import BaseSchema, PaginationSchema


class GetProfileListSchema(PaginationSchema):
    name = fields.String()
    code = fields.String()
    position = fields.String()

    
class ProfileSchema(BaseSchema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    position = fields.String(required=True, validate=validate.Length(min=1, max=200))
    code = fields.String(required=True, validate=validate.Length(min=1, max=10))
    images = fields.List(fields.String)
