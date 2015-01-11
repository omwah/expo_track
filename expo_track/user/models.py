from flask.ext.login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from ..app import db, login_manager
from ..utils import get_current_time

user_permissions = db.Table('user_permissions',
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    'A person who logs into the system and has certain privileges'

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    created_time = db.Column(db.DateTime, default=get_current_time, nullable=False)
    last_modified = db.Column(db.DateTime, default=get_current_time, onupdate=get_current_time, nullable=False)

    name = db.Column(db.String(32), unique=True, nullable=False)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person', backref=db.backref('user', lazy='dynamic'), uselist=False)

    # Password data and methods
    _password = db.Column('password', db.String(128), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(User.name == login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    permissions = db.relationship('Permission', secondary=user_permissions, lazy='dynamic', backref=db.backref('users', lazy='dynamic'))

    def has_permission(self, name):
        'Check out whether a user has a permission or not.'

        permission = Permission.query.filter_by(name=name).first()
        # if the permission does not exist or was not given to the user
        if not permission or not permission in self.permissions:
            return False
        return True

    def grant_permission(self, name):
        'Grant a permission to a user.'
        permission = Permission.query.filter_by(name=name).first()
        if permission and permission in self.permissions:
            return
        elif not permission:
            raise ValueError('%s is not a valid permission type' % name)
        self.permissions.append(permission)

    def revoke_permission(self, name):
        'Revoke a given permission for a user.'
        permission = Permission.query.filter_by(name=name).first()
        if not permission or not permission in self.permissions:
            return
        self.permissions.remove(permission)

class Permission(db.Model):
    'Permissions attatched to a user'

    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True, unique=True)
    description = db.Column(db.String(1024), nullable=False)

def create_permission_types():
    'Create permission types, should only be called on database initialziation'

    # Add privilege for being able to perform an action associated
    # with an item such as check in or check out
    perm_types = [ 
            ('perform_action', 'Can perform actions such ask checking in or out items') ]

    # Add an add_, edit_ and del_ permission for each of these types
    # of data
    add_edit_del_types = { 
            'item': 'Can %s items',
            'person': 'Can %s people',
            'event': 'Can %s events',
            'location': 'Can %s locations',
            'team': 'Can %s teams',
            'user': 'Can %s users',
    }
    for aed_type, desc_template in add_edit_del_types.items():
        for prefix in ('add', 'edit', 'delete'):
            perm_types.append( ('%s_%s' % (prefix, aed_type), desc_template % prefix) )

    # Users have additional view permission as you don't want everyone and
    # their buddy knowing who the other users are
    perm_types.append( ('view_user', 'Can view users') )

    for ptype, pdesc in perm_types:
        db.session.add(Permission(name=ptype, description=pdesc))
    db.session.commit()

# Login Manager callbacks

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@login_manager.request_loader
def load_user_from_request(request):
    'Log in user using BasicAuth'

    auth = request.authorization
    # We need to ignore authentication headers for OPTIONS to avoid
    # unwanted interactions with CORS.
    # Chrome and Firefox issue a preflight OPTIONS request to check
    # Access-Control-* headers, and will fail if it returns 401.
    if request.method != 'OPTIONS':
        if auth:
            result = User.authenticate(auth.username, auth.password)
            # Return user object only if authenfication is successful
            if result[1]:
                return result[0]
    
    # finally, return None if BasicAuth did not work
    return None
