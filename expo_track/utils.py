from datetime import datetime
from flask.ext.restful import fields

from app import db

def get_current_time():
    return datetime.utcnow()

class SafeUrlField(fields.Url):
    """
    A Flask-Restful field that does not cause an exception when used
    in a Nested field to compute a url. Instead just returns None.
    """
    def output(self, key, obj):
        if obj == None:
            return None
        else:
            # Refresh the object. After a commit an object
            # will be expired and when doing a Restful marshal
            # this will fail unless the object has been refreshed
            # if somehow the uri field is the first computed.
            # This error would occur based on the dictonary
            # ordering of fields used with marshal()
            # Rare annoying error that was..
            db.session.refresh(obj)
            return super(SafeUrlField, self).output(key, obj)

# Allow id to be either an integer or None
def int_or_none(value):
    if value == None:
        return None
    else:
        return int(value)
