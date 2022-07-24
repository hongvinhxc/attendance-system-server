from mongoengine import NotUniqueError, DoesNotExist, ValidationError

from application.log_handlers import logger
from application.models.export_report import ExportReport
from application.services import BaseService


class ExportReportService(BaseService):
    def __init__(self):
        pass

    
    def count_export_reports(self, filter = {}):
        """
        count export reports
        """
        filter = self.build_regex(filter)
        count = ExportReport.objects(**filter).count()
        return count

    def save_export_report(self, doc):
        """
        save export report
        """
        try:
            export_report = ExportReport(**doc)
            export_report.save()
            return True, self.to_dict(export_report)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message

    def get_export_reports(self, limit, offset, filter = {}):
        """
        get export report
        """
        try:
            filter = self.build_regex(filter)
            export_reports = ExportReport.objects(**filter).limit(limit).skip(offset)
            return self.to_dict(list(export_reports))
        except Exception as error:
            logger.error(error)
        return []

    def delete_export_report(self, export_report_id):
        """
        delete a export report by id
        """
        try:
            export_report = ExportReport.objects.get(id=export_report_id)
            export_report.delete()
            return True, "Delete export report successful"
        except DoesNotExist as error:
            error_message = "An export report with this id does not exist"
            logger.error(error)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message

    def get_export_report(self, export_report_id):
        """
        get a export report by id
        """
        try:
            export_report = ExportReport.objects.get(id=export_report_id)
            return True, self.to_dict(export_report)
        except ValidationError as error:
            error_message = error.message
            logger.error(error)
        except DoesNotExist as error:
            error_message = "An export report with this id does not exist"
            logger.error(error)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message