import logging
from application import config
from application.models.auth import Auth


logger = logging.getLogger(config.CloudPortalApi.APP_NAME)

class AuthService():
    def __init__(self):
        pass

    def add_account(self, doc):
        """
        add account
        """
        try:
            auth = Auth(**doc)
            auth.save()
            return auth.id
        except Exception as error:
            logger.error(error)
        return False
    
    def find_account_by_username(self, username) -> Auth:
        """
        find account by username
        """
        try:
            result = Auth.objects(username=username).first()
            return result
        except Exception as error:
            logger.error(error)
        return False
