import os
_base_dir = os.path.abspath(os.path.dirname(__file__))
_instance_dir = os.path.join(_base_dir, "instance")

DEBUG = True

# Site administrators contact information
ADMINS = frozenset(['youremail@yourdomain.com'])

# Used to sign cookies, change for production
SECRET_KEY = 'This string will be replaced with a proper key in production.'

# Database Options
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_instance_dir, 'expo_track.db')
DATABASE_CONNECT_OPTIONS = {}

# For WTF Forms, change key for production
CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"
