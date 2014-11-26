from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext import restful

# Setup application
app = Flask(__name__)
app.config.from_object('config')

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Setup database
db = SQLAlchemy(app)

# Handle errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Restful API
api = restful.Api(app)

# Add API resources
from .user.api import Login
api.add_resource(Login, '/api/login', endpoint='login')

# Add Blueprints to application
from .interface.views import mod as interface_mod
app.register_blueprint(interface_mod)
