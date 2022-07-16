from unittest import result
from flask import send_file
from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required
from application.controllers.attendance import AttendanceController
from application.schemas.attendance import ExportAttendanceSchema, GetAttendanceDetailSchema, GetAttendanceListSchema
from helpers import pack_result

ns = Namespace('attendance')


@ns.route('')
class Attendance(Resource):

    @jwt_required()
    @use_args(GetAttendanceListSchema(), location='query')
    def get(self, args):
        result = AttendanceController().get_attendances(args)
        return pack_result(status=True, data=result)


@ns.route('/export')
class ExportAttendance(Resource):

    @jwt_required()
    @use_args(ExportAttendanceSchema())
    def post(self, args):
        status, result = AttendanceController().export_attendances(args)
        if status: 
            return send_file(result) 
        return pack_result(status=False, message=result)


@ns.route('/<string:profile_id>')
class AttendanceDetail(Resource):

    @jwt_required()
    @use_args(GetAttendanceDetailSchema(), location='query')
    def get(self, args, **kwargs):
        month = args["month"]
        profile_id = kwargs["profile_id"]
        status, result = AttendanceController().get_profile_attendances_by_month(profile_id, month)
        if status: 
            return pack_result(status=True, data=result)
        return pack_result(status=False, message=result)