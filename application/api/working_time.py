from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required

from application.controllers.working_time import WorkingTimeController
from application.schemas.working_time import WorkingTimeSchema
from helpers import pack_result


ns = Namespace('working-time')


@ns.route('')
class WorkingTime(Resource):

    @jwt_required()
    def get(self):
        status, result = WorkingTimeController().get_working_time()
        if status: 
            return pack_result(status=True, data=result)
        return pack_result(status=False, message=result)

    @jwt_required()
    @use_args(WorkingTimeSchema())
    def post(self, args):
        status, result = WorkingTimeController().update_working_time(args)
        return pack_result(status=status, message=result)
