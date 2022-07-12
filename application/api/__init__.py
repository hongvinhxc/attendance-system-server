from flask import Blueprint, Flask
from flask_restx import Api

from .auth import ns as auth_ns
from .profile import ns as profile_ns
from .detect_face import ns as detect_face_ns

def init_app(app: Flask):

    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(blueprint, version='1.0', title='Attendance Portal API')

    app.register_blueprint(blueprint)

    # add namespace bellow here
    api.add_namespace(auth_ns)
    api.add_namespace(profile_ns)
    api.add_namespace(detect_face_ns)
