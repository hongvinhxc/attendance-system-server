from marshmallow import EXCLUDE, Schema, fields

class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

class PaginationSchema(BaseSchema):
    size = fields.Int(load_default=10)
    page = fields.Int(load_default=1)