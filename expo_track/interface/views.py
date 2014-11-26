from flask import Blueprint, render_template
from flask.ext.login import login_required

# Root level of application
mod = Blueprint('interface', __name__, url_prefix='')

@mod.route('/')
@login_required
def index():
    return render_template('interface/index.html')
