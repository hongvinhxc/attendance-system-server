from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required

from application.controllers.profile import ProfileController
from application.schemas.profile import GetProfileListSchema, ProfileSchema
from helpers import pack_result


ns = Namespace('profiles')


@ns.route('')
class Profile(Resource):

    @jwt_required()
    @use_args(GetProfileListSchema(), location='query')
    def get(self, args):
        result = ProfileController().get_profiles(args)
        return pack_result(status=True, data=result)

    @jwt_required()
    @use_args(ProfileSchema())
    def post(self, args):
        status, result = ProfileController().add_profile(args)
        if status: 
            return pack_result(status=True, data=result, message="Create user successful")
        return pack_result(status=False, message=result)


@ns.route('/<string:profile_id>')
class ProfileDetail(Resource):

    @jwt_required()
    def get(self, **kwargs):
        profile_id = kwargs['profile_id']
        status, result = ProfileController().get_profile(profile_id)
        if status: 
            return pack_result(status=True, data=result)
        return pack_result(status=False, message=result)
        
    @jwt_required()
    @use_args(ProfileSchema())
    def put(self, args, **kwargs):
        profile_id = kwargs['profile_id']
        status, result = ProfileController().update_profile(profile_id, args)
        return pack_result(status, message=result)
        
    @jwt_required()
    def delete(self, **kwargs):
        profile_id = kwargs['profile_id']
        status, result = ProfileController().delete_profile(profile_id)
        return pack_result(status=status, message=result)


@ns.route('/get-images/<string:profile_id>')
class ProfileDetail(Resource):

    @jwt_required()
    def get(self, **kwargs):
        profile_id = kwargs['profile_id']
        status, result = ProfileController().get_profile_images(profile_id)
        if status: 
            return pack_result(status=True, data=result)
        return pack_result(status=False, message=result)