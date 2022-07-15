from flask import jsonify
from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args

from application.controllers.detect_face import DetectFaceController
from application.schemas.detect_face import DetectFaceSchema
from helpers import pack_result


ns = Namespace('detect-face')


@ns.route('')
class Profile(Resource):

    @use_args(DetectFaceSchema())
    def post(self, args):
        image = args["image"]
        status, result = DetectFaceController().predict_face(image)
        if status: 
            return pack_result(status=True, data=result)
        return pack_result(status=False, message=result)