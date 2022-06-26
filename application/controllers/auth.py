
import argon2
import logging
from application import config
from application.services.auth import AuthService
from flask_jwt_extended import create_access_token


logger = logging.getLogger(config.CloudPortalApi.APP_NAME)

argon2_hasher = argon2.PasswordHasher(
    time_cost=3, # number of iterations
    memory_cost=64 * 1024, # 64mb
    parallelism=1, # how many parallel threads to use
    hash_len=32, # the size of the derived key
    salt_len=16 # the size of the random generated salt in bytes
)

class AuthController():

    def __init__(self) -> None:
        self.auth_service = AuthService()

    def login(self, username, password):
        """
        login and return jwt token
        """
        resp_error = {
            "status": False,
            "message": "Wrong username or password"
        }
        account = self.find_account_by_username(username)
        if not account:
            return None, resp_error
        
        hash = account.password
        
        verify_valid = self.verify_password(hash, password)
        if not verify_valid:
            return None, resp_error

        access_token = create_access_token(identity=username)
        return access_token, {
            "status": True,
            "message": "Login successful"
        }

    def add_account(self, doc):
        doc['password'] = self.hash_password(doc['password'])
        return self.auth_service.add_account(doc)

    def find_account_by_username(self, username):
        """
        find account by username
        """
        return self.auth_service.find_account_by_username(username)

    def hash_password(self, password):
        """
        generate hash for password before save to database 
        """
        hash = argon2_hasher.hash(password) 
        return hash

    def verify_password(self, hash, password):
        """
        verify password with hash
        """
        try:
            return argon2_hasher.verify(hash, password)
        except argon2.exceptions.VerifyMismatchError as error:
            logger.error(error)
        return False