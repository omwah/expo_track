from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

# Setup application
app = Flask(__name__)
app.config.from_object('config')

# Setup database
db = SQLAlchemy(app)

# Handle errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from .interface.views import mod as interface_module
app.register_blueprint(interface_module)
