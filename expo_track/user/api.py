from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import current_user, login_user, logout_user, login_required

from models import User

from ..person.api import person_fields

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

class PermissionField(fields.Raw):
    def format(self, value):
        return [ p.name for p in value ]

profile_fields = {
    'name': fields.String,
    'person': fields.Nested(person_fields),
    'permissions': PermissionField,
}

class ProfileResource(Resource):
    'Information for current_user about theirself'

    @login_required
    @marshal_with(profile_fields)
    def get(self):
        return current_user

def register_api(api):
    api.add_resource(LoginResource, '/api/login', endpoint='login')
    api.add_resource(ProfileResource, '/api/profile', endpoint='profile')
