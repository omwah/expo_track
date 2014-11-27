from flask.ext.restful import Resource, reqparse
from flask.ext.login import current_user, login_user, logout_user

from models import User

class LoginResource(Resource):
    'Allow login via the API to get the session cookie'

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('remember_me', type=bool)

    def get(self):
        if not current_user.is_anonymous() and current_user.is_authenticated:
            return { 'username': current_user.name, 'authenticated': True }
        else:
            return { 'authenticated': False }, 401

    def delete(self):
        if current_user.is_authenticated:
            logout_user()
        # Don't return an error code since not being authenticated
        # is what is desired
        return { 'authenticated': False }

    def post(self):
        args = self.parser.parse_args()

        user, authenticated = User.authenticate(args.username, args.password)
        if authenticated:
            login_user(user, remember=args.remember_me)
            return { 'username': user.name, 'authenticated': True }
        else:
            return { 'authenticated': False }, 401 

def register_api(api):
    api.add_resource(LoginResource, '/api/login', endpoint='login')
