from mongoengine import DoesNotExist, ValidationError

from application.log_handlers import logger
from application.models.working_time import WorkingTime
from application.services import BaseService


class WorkingTimeService(BaseService):
    def __init__(self):
        pass
  
    def get_working_time(self):
        """
        get working time
        """
        try:
            working_time = WorkingTime.objects.get()
            return True, self.to_dict(working_time)
        except DoesNotExist as error:
            error_message = "Working time does not exist. Let setting up it."
            logger.error(error)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message

    
    def update_working_time(self, doc):
        """
        update working time
        """
        try:
            working_time = WorkingTime.objects(type="config")
            working_time.update(upsert=True, **doc)
            return True, "Update working time successful"
        except ValidationError as error:
            error_message = error.message
            logger.error(error)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message