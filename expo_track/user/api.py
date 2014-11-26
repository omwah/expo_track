from flask import request

from flask.ext.restful import Resource, reqparse
from flask.ext.login import login_user

from models import User

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        args = self.parser.parse_args()

        user, authenticated = User.authenticate(args.username, args.password)
        if authenticated:
            login_user(user)
            return { 'username': user.name, 'authenticated': True }
        else:
            return { 'authenticated': False }, 401 
