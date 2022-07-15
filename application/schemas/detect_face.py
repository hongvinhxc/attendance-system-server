from marshmallow import fields

from application.schemas import BaseSchema

    
class DetectFaceSchema(BaseSchema):
    image = fields.String(required=True)
