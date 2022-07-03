from application.log_handlers import logger
from application.models.auth import Auth
from application.services import BaseService


class AuthService(BaseService):
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
