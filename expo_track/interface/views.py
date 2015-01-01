from flask import Blueprint, render_template
from flask.ext.login import current_user, login_required

from ..item.constants import STATUS_TYPES, STATUS_COMMAND_NAMES, STATUS_OPPOSITES
from ..person.constants import CONTACT_TYPES
from ..user.models import Permission

# Root level of application
mod = Blueprint('interface', __name__, url_prefix='')

@mod.route('/')
def index():
    return render_template('interface/index.html',
            status_types=STATUS_TYPES,
            status_command_names=STATUS_COMMAND_NAMES.items(),
            status_opposites=STATUS_OPPOSITES)

@mod.route('/config')
@login_required
def config():
    def perm_compare(a, b):
        'Sort based on type of permission, that being the second part of the name'
        type_a = a.split("_")[1]
        type_b = b.split("_")[1]
        if type_a == type_b:
            return cmp(a, b)
        else:
            return cmp(type_a, type_b)

    permissions = sorted([ p.name for p in Permission.query.all() ], cmp=perm_compare)

    return render_template('interface/config.html', current_user=current_user, contact_types=CONTACT_TYPES.items(), permissions=permissions)
