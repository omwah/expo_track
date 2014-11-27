from functools import wraps

from flask import abort
from flask.ext.login import current_user

def can_edit_items(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.can_edit_items:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def can_perform_action(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.can_perform_action:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def can_edit_people(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.can_edit_people:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def can_edit_events(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.can_edit_events:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def can_edit_locations(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.can_edit_locations:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def can_edit_teams(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.can_edit_teams:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
