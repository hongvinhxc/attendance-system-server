from marshmallow import fields

from application.schemas import BaseSchema


class LoginSchema(BaseSchema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)

class ChangePasswordSchema(BaseSchema):
    password = fields.String(required=True, allow_none=False)
    new_password = fields.String(required=True, allow_none=False)