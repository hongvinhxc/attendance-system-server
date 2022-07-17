from datetime import timedelta
from dateutil import relativedelta
from mongoengine import NotUniqueError, DoesNotExist, ValidationError
from application.constants import DAY_IN_CALENDAR

from application.log_handlers import logger
from application.models.attendance import Attendance
from application.services import BaseService


class AttendanceService(BaseService):
    def __init__(self):
        pass
  
    def get_profile_attendance_by_day(self, id, day):
        """
        get profile attendance by date
        """
        try:
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(hours=24)
            query = {
                "profile_id": id,
                "creation_date__gte": day_start,
                "creation_date__lt": day_end
            }
            result = Attendance.objects.get(**query)
            return True, result
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message

    def get_profile_attendances_by_month(self, id, month):
        """
        get profile attendances by month
        """
        try:
            day_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + relativedelta.relativedelta(months=1)
            query = {
                "profile_id": id,
                "creation_date__gte": day_start,
                "creation_date__lt": day_end
            }
            result = Attendance.objects(**query)
            return True, result
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message

    def get_profile_attendances_by_month_for_calendar(self, id, month):
        """
        get profile attendances by month
        """
        try:
            day_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            day_start = day_start - relativedelta.relativedelta(days=(day_start.weekday() + 1) % 7)
            day_end = day_start + relativedelta.relativedelta(days=DAY_IN_CALENDAR)
            query = {
                "profile_id": id,
                "creation_date__gte": day_start,
                "creation_date__lt": day_end
            }
            result = Attendance.objects(**query)
            return True, result
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message
        
    def add_attendance(self, doc):
        """
        add attendance
        """
        try:
            attendance = Attendance(**doc)
            attendance.save()
            return True, self.to_dict(attendance)
        except NotUniqueError as error:
            error_message = "An employee with this employee code already exists"
            logger.error(error)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message

    def update_attendance(self, attendance_id, doc):
        """
        update attendance
        """
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            attendance.update(**doc)
            return True, "Update attendance successful"
        except ValidationError as error:
            error_message = error.message
            logger.error(error)
        except DoesNotExist as error:
            error_message = "An employee with this id does not exist"
            logger.error(error)
        except NotUniqueError as error:
            error_message = "An employee with this employee code already exists"
            logger.error(error)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message