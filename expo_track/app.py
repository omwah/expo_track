from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

# Setup application
app = Flask(__name__)
app.config.from_object('config')

# HTTP Basic Authentification. Protect with HTTPS to secure
auth  = HTTPBasicAuth()

# Setup database
db = SQLAlchemy(app)

# Handle errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Register modules
from .interface.views import mod as interface_module
app.register_blueprint(interface_module)
