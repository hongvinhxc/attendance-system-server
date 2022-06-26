from marshmallow import Schema, fields


class LoginParameters(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)