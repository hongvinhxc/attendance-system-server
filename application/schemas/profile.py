from marshmallow import Schema, fields


class ProfileParameters(Schema):
    name = fields.String(required=True)