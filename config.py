import os, platform

_base_dir = os.path.abspath(os.path.dirname(__file__))

INSTANCE_DIR = os.path.join(_base_dir, "instance")

DEBUG = True

# Site administrators contact information, by default just <username>@<hostname>
try:
    ADMINS = frozenset(['%s@%s' % (os.getlogin(), platform.node())])
except OSError as exc:
    # In case os.getlogin() fails
    ADMINS = frozenset(['%s@%s' % (os.environ['USER'], platform.node())])

# Used to sign cookies, change for production
SECRET_KEY = 'This string will be replaced with a proper key in production.'

# Database Options
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_DIR, 'expo_track.db')
