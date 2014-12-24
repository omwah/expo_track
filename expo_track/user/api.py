from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import current_user, login_user, logout_user, login_required

from ..app import db
from ..utils import SafeUrlField
from ..user.decorators import has_permission

from models import User, Permission
from ..person.api import nested_person_fields

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
    'person': fields.Nested(nested_person_fields),
    'permissions': PermissionField,
}

class ProfileResource(Resource):
    'Information for current_user about theirself'

    @login_required
    @marshal_with(profile_fields)
    def get(self):
        return current_user


user_fields = {
    'id': fields.String,
    'name': fields.String,
    'person': fields.Nested(nested_person_fields),
    'permissions': PermissionField,
    'uri': SafeUrlField('user'),
}

def user_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('person_id', type=str, required=True)
    parser.add_argument('password', type=str)
    parser.add_argument('permissions', type=str, action='append', default=[])
    return parser 

def modify_permissions(user, perm_strings):
    # Handle easy case where all permissions have been removed
    if len(perm_strings) == 0:
        user.permissions = []
        return

    # Get objects that are associated with perm_strings strings
    perm_objs = []
    for perm_name in perm_strings:
        perm = Permission.query.filter(Permission.name == perm_name).first()
        if perm != None:
            perm_objs.append(perm)

    # Delete non existent permissions in list passed
    for existing_perm in user.permissions:
        if not existing_perm in perm_objs:
            user.permissions.remove(existing_perm)

    # Add any new permissions
    for passed_perm in perm_objs:
        if not passed_perm in user.permissions:
            user.permissions.append(passed_perm)

class UserListResource(Resource):

    @login_required
    @has_permission('view_user')
    @marshal_with(user_fields)
    def get(self):
        return User.query.all()
    
    @login_required
    @has_permission('add_user')
    @marshal_with(user_fields)
    def post(self):
        args = user_parser().parse_args()

        user = User(name=args.name,
                person_id=args.person_id,
                password=args.password)

        modify_permissions(user, args.permissions)

        db.session.add(user)
        db.session.commit()

        return user
        
class UserResource(Resource):

    @login_required
    @has_permission('view_user')
    @marshal_with(user_fields)
    def get(self, id):
        return User.query.filter(User.id == id).first_or_404()

    @login_required
    @has_permission('edit_user')
    @marshal_with(user_fields)
    def put(self, id):
        args = user_parser().parse_args()

        user = User.query.filter(User.id == id).first_or_404()

        user.name = args.name
        user.person_id = args.person_id

        # Only change when supplied
        if args.password != None:
            user.password = args.password

        modify_permissions(user, args.permissions)

        db.session.commit()

        return user
        
    @login_required
    @has_permission('delete_user')
    def delete(self, id):
        user = User.query.filter(User.id == id).first_or_404()

        db.session.delete(user)
        db.session.commit()

        return { 'delete': True }

def register_api(api):
    api.add_resource(LoginResource, '/api/login', endpoint='login')
    api.add_resource(ProfileResource, '/api/profile', endpoint='profile')

    api.add_resource(UserListResource, '/api/users', endpoint='users_list')
    api.add_resource(UserResource, '/api/users/<int:id>', endpoint='user')
