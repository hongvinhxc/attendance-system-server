import os

class PortalApi(object):
    FILENAME = __file__

    APP_NAME = "attendance-system"
    
    FLASK_ENV = 'development'
    DEBUG = True
    PORT = 8888

    JWT_SECRET_KEY = "this text is secret key"
    JWT_TOKEN_LOCATION = "cookies"
    JWT_ACCESS_TOKEN_EXPIRES = 30 * 60
    JWT_ERROR_MESSAGE_KEY = "message"

    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"
    LOG_FOLDER = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'logs')

    MONGODB_SETTINGS = [
        {
            'ALIAS': 'default',
            'DB': 'attendance-system',
            'USERNAME': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 27017
        }
    ]

    CONFIDENCE = 0.6
    DISTANCE_THRESHOLD = 0.5

    DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'application', 'data')
    REPORTS_FOLDER_PATH = os.path.join(DATA_PATH, 'reports')
    IMAGES_FOLDER_PATH = os.path.join(DATA_PATH, 'profile-images')
    MODEL_FOLDER_PATH = os.path.join(DATA_PATH, 'model')
    PROTOTXT_PATH = os.path.join(MODEL_FOLDER_PATH, "deploy.prototxt")
    CAFFEMODEL_PATH = os.path.join(MODEL_FOLDER_PATH, "weights.caffemodel")
    MODEL_TRAINED_PATH = os.path.join(DATA_PATH, "model.clf")