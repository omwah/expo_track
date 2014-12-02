from flask import Blueprint, render_template
from flask.ext.login import login_required

from ..item.constants import STATUS_TYPES

# Root level of application
mod = Blueprint('interface', __name__, url_prefix='')

@mod.route('/')
def index():
    return render_template('interface/index.html', status_types=STATUS_TYPES.items())
