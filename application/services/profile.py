from mongoengine import NotUniqueError, DoesNotExist, ValidationError

from application.log_handlers import logger
from application.models.profile import Profile
from application.services import BaseService


class ProfileService(BaseService):
    def __init__(self):
        pass

    def count_profiles(self, filter = {}):
        """
        count profiles
        """
        filter = self.build_regex(filter)
        count = Profile.objects(**filter).count()
        return count
  
    def get_profiles(self, limit, offset, filter = {}):
        """
        get profile
        """
        filter = self.build_regex(filter)
        profiles = Profile.objects(**filter).limit(limit).skip(offset)
        return self.to_dict(list(profiles))

    def add_profile(self, doc):
        """
        add profile
        """
        try:
            profile = Profile(**doc)
            profile.save()
            return True, self.to_dict(profile)
        except NotUniqueError as error:
            error_message = "An employee with this employee code already exists"
            logger.error(error)
        except Exception as error:
            error_message = error
            logger.error(error)
        return False, error_message
    
    def update_profile(self, profile_id, doc):
        """
        update profile
        """
        try:
            print(doc)
            profile = Profile.objects.get(id=profile_id)
            profile.update(**doc)
            # profile.save()
            return True, "Update profile successfull"
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
            error_message = error
            logger.error(error)
        return False, error_message

    def get_profile(self, profile_id):
        """
        get a profile by id
        """
        try:
            profile = Profile.objects.get(id=profile_id)
            return True, self.to_dict(profile)
        except ValidationError as error:
            error_message = error.message
            logger.error(error)
        except DoesNotExist as error:
            error_message = "An employee with this id does not exist"
            logger.error(error)
        except Exception as error:
            error_message = error
            logger.error(error)
        return False, error_message