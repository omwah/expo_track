from flask import Blueprint, render_template
from flask.ext.login import current_user, login_required

from ..item.constants import STATUS_TYPES
from ..person.constants import CONTACT_TYPES

# Root level of application
mod = Blueprint('interface', __name__, url_prefix='')

@mod.route('/')
def index():
    return render_template('interface/index.html', status_types=STATUS_TYPES.items())

@mod.route('/config')
@login_required
def config():
    return render_template('interface/config.html', current_user=current_user, contact_types=CONTACT_TYPES.items())
