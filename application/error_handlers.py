
from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import default_exceptions, HTTPException, UnprocessableEntity, InternalServerError
from webargs.flaskparser import parser

from . log_handlers import logger

def init_app(app: Flask):
    """Configures the error handlers."""

    parser.error_handler(webargs_error_handler)

    for exception in default_exceptions:
        app.register_error_handler(exception, exception_error_handler)

    app.register_error_handler(Exception, exception_error_handler)

def webargs_error_handler(err: ValidationError, *args, **kwargs):
    """
    Flask-RESTX will try to jsonify the data attribute of the raised HTTPError.
    In webargs, the data attribute contains the ValidationError object, which 
    is not JSON-serializable. 

    Just raise UnprocessableEntity error for app error handlers, not auto jsonify
    :param err: marshmallow.exceptions.ValidationError
    :raise: error
    """
    raise UnprocessableEntity(description=err.normalized_messages())

def exception_error_handler(error):
    """
    Catch error and return response.
    """
    if not isinstance(error, HTTPException):
        logger.exception(error)
        error = InternalServerError()

    status_code = error.code
    message = error.description

    return jsonify(message=message), status_code
