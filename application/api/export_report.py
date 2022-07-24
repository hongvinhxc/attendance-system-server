from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required
from flask import send_from_directory
from application import config

from application.controllers.export_report import ExportReportController
from application.schemas.export_report import GetExportReportListSchema, ExportReportSchema
from helpers import pack_result


ns = Namespace('export-report')


@ns.route('')
class Profile(Resource):

    @jwt_required()
    @use_args(GetExportReportListSchema(), location='query')
    def get(self, args):
        result = ExportReportController().get_reports(args)
        return pack_result(status=True, data=result)

    @jwt_required()
    @use_args(ExportReportSchema())
    def post(self, args):
        status, result = ExportReportController().export_report(args)
        if status: 
            return send_from_directory(config.PortalApi.REPORTS_FOLDER_PATH, result)
        return pack_result(status=False, message=result)


@ns.route('/<string:report_id>')
class ProfileDetail(Resource):

    @jwt_required()
    def get(self, **kwargs):
        report_id = kwargs['report_id']
        status, result = ExportReportController().download_export_report(report_id)
        if status: 
            return send_from_directory(config.PortalApi.REPORTS_FOLDER_PATH, result)
        return pack_result(status=False, message=result)
        
        
    @jwt_required()
    def delete(self, **kwargs):
        report_id = kwargs['report_id']
        status, result = ExportReportController().delete_export_report(report_id)
        return pack_result(status=status, message=result)

