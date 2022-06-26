import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from application import config


logger = logging.getLogger(config.CloudPortalApi.APP_NAME)

def init_app(app: Flask):
    """
    Config log
    :param app: flask app
    :return: not return
    """
    format_prefix = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    formatter = logging.Formatter(format_prefix)

    info_log = os.path.join(app.config['LOG_FOLDER'], app.config['INFO_LOG'])
    info_file_handler = RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.DEBUG)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(app.config['LOG_FOLDER'], app.config['ERROR_LOG'])
    error_file_handler = RotatingFileHandler(error_log, maxBytes=100000, backupCount=10)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    # set proper log level
    app.logger.setLevel(logging.DEBUG if app.debug else logging.WARN)

    # unify log format for all handers
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)

    app.logger.info('Config filename: {0}'.format(app.config['FILENAME']))
    app.logger.error('App log folder: {0}'.format(app.config['LOG_FOLDER']))