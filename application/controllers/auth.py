
import argon2
import re
import logging
from application import config
from application.services.auth import AuthService
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity


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

    def change_password(self, password, new_password):
        """
        change user password
        """
        username = get_jwt_identity()
        account = self.find_account_by_username(username)
        hash = account.password
        verify_valid = self.verify_password(hash, password)
        if not verify_valid:
            return {
                "status": False,
                "message": "Wrong password"
            }

        is_old_password = next(filter(lambda hash: self.verify_password(hash, new_password), account.password_history), None)
        if is_old_password:
            return {
                "status": False,
                "message": "Password must not be old password"
            }

        is_strong_password = self.check_strong_password(new_password)
        if not is_strong_password:
            return {
                "status": False,
                "message": "Password must be at least 8 characters include uppercase and lowercase letters, numbers and symbols"
            }

        account['password'] = self.hash_password(new_password)
        account.save()

        return {
            "status": True,
            "message": "Change password successful"
        }

    def check_strong_password(self, password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """

        # calculating the length
        length_error = len(password) < 8

        # searching for digits
        digit_error = re.search(r"\d", password) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None

        # searching for symbols
        symbol_error = re.search(r"[@ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

        # overall result
        password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

        return password_ok