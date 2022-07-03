from urllib import response
from flask import jsonify
from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required

from application.controllers.profile import ProfileController
from application.schemas.profile import GetProfileListParameters, ProfileParameters


ns = Namespace('profiles')


@ns.route('/')
class Profile(Resource):

    @jwt_required()
    @use_args(GetProfileListParameters(), location='query')
    def get(self, args):
        result = ProfileController().get_profiles(args)
        return jsonify(success=True, data=result)

    @jwt_required()
    @use_args(ProfileParameters())
    def post(self, args):
        status, result = ProfileController().add_profile(args)
        response = {
            "status": status
        }
        if status: 
            response['data'] = result
            response['message'] = "Create user successful"
        else:
            response['message'] = result
        return jsonify(response)


@ns.route('/<string:profile_id>')
class ProfileDetail(Resource):

    @jwt_required()
    def get(self, **kwargs):
        profile_id = kwargs['profile_id']
        status, result = ProfileController().get_profile(profile_id)
        response = {
            "status": status
        }
        if status: 
            response['data'] = result
        else:
            response['message'] = result
        return jsonify(response)
        
    @jwt_required()
    @use_args(ProfileParameters())
    def post(self, args, **kwargs):
        profile_id = kwargs['profile_id']
        status, result = ProfileController().update_profile(profile_id, args)
        return jsonify(success=status, data=result)