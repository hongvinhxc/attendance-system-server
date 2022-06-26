from flask import jsonify
from flask_restx import Resource, Namespace
from webargs.flaskparser import use_args
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import jwt_required

from application.controllers.auth import AuthController
from application.schemas.auth import LoginParameters


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
        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)
        return response