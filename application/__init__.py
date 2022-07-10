from flask import Flask
from flask_cors import CORS
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies

from application import api
from application import config
from application import models
from application import log_handlers
from application import error_handlers


def create_app(config_object=None):
    app = Flask(config.PortalApi.APP_NAME)
    CORS(app)

    app.config.from_object(config.PortalApi)
    app.config.from_object(config_object)

    configure_extensions(app)
    configure_log_handlers(app)
    configure_error_handlers(app)
    configure_blueprints(app)

    JWTManager(app)
    
    return app

def configure_extensions(app: Flask):
    models.init_app(app)

def configure_blueprints(app: Flask):
    api.init_app(app)

    @app.after_request
    def refresh_expiring_jwts(response):
        """
        Refresh any token that is within 5 minutes of expiring
        """
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(seconds=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            return response

def configure_log_handlers(app: Flask):
    log_handlers.init_app(app) 

def configure_error_handlers(app: Flask):
    error_handlers.init_app(app)

