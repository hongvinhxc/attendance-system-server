from flask import jsonify
from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required

from application.controllers.profile import ProfileController
from application.schemas.profile import ProfileParameters


ns = Namespace('profiles')


@ns.route('/')
class Profile(Resource):

    @jwt_required()
    def get(self):
        result = ProfileController().get_profiles()
        return jsonify(data=result)

    @jwt_required()
    def post(self, args, **kwargs):
        return ProfileController().add_profile({})


@ns.route('/<string:profile_id>')
class ProfileDetail(Resource):

    @jwt_required()
    def get(self, **kwargs):
        return  {"kwargs": kwargs}
        
    @jwt_required()
    @use_args(ProfileParameters(), location='json')
    def put(self, args, **kwargs):
        return {"args": args, "kwargs": kwargs}