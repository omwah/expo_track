from functools import wraps

from flask import abort
from flask.ext.login import current_user

def has_permission(perm_name):
    def perm_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(perm_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return perm_decorator
