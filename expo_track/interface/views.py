from flask import Blueprint, render_template

# Root level of application
mod = Blueprint('interface', __name__, url_prefix='')

@mod.route('/')
def index():
    return render_template('interface/index.html')
