from datetime import datetime
from flask.ext.restful import fields

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
            return super(SafeUrlField, self).output(key, obj)
