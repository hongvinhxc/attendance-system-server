from datetime import timedelta
from mongoengine import NotUniqueError, DoesNotExist, ValidationError

from application.log_handlers import logger
from application.models.attendance import Attendance
from application.services import BaseService


class AttendanceService(BaseService):
    def __init__(self):
        pass
  
    def get_profile_attendance_by_day(self, id, day):
        """
        get profile by date
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