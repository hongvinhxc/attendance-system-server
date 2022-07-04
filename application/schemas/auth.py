from marshmallow import fields

from application.schemas import BaseSchema


class LoginParameters(BaseSchema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)

class ChangePasswordParameters(BaseSchema):
    password = fields.String(required=True, allow_none=False)
    new_password = fields.String(required=True, allow_none=False)