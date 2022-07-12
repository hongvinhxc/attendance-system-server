from flask import jsonify
from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import jwt_required

from application.controllers.auth import AuthController
from application.schemas.auth import LoginParameters, ChangePasswordParameters
from helpers import pack_result


ns = Namespace('auth')


@ns.route('/login')
class Login(Resource):

    @use_args(LoginParameters())
    def post(self, args):
        username = args["username"]
        password = args["password"]
        access_token, result = AuthController().login(username, password)
        response = jsonify(result)
        if access_token:
            set_access_cookies(response, access_token)
        return response


@ns.route('/logout')
class Logout(Resource):

    @jwt_required()
    def get(self):
        response = pack_result(True, "Logout successful")
        unset_jwt_cookies(response)
        return response


@ns.route('/change-password')
class ChangPassword(Resource):

    @jwt_required()
    @use_args(ChangePasswordParameters())
    def post(self, args):
        password = args["password"]
        new_password = args["new_password"]
        result = AuthController().change_password(password, new_password)
        response = jsonify(result)
        return response