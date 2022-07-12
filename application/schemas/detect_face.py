from marshmallow import fields

from application.schemas import BaseSchema

    
class DetectFaceParameters(BaseSchema):
    image = fields.String(required=True)
