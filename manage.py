#!/usr/bin/env python

import os

from flask.ext.script import Command, Manager, Shell

from expo_track import app, db, models

manager = Manager(app)

@manager.command
def initdb():
    'Resets the database tables.'

    if not os.path.exists(app.config['INSTANCE_DIR']):
        os.makedirs(app.config['INSTANCE_DIR'])

    db.drop_all()
    db.create_all()

    # Add user permission types
    from expo_track.user.models import create_permission_types
    create_permission_types()

    db.session.commit()

def _make_context():
    return dict(app=app, db=db, models=models)

manager.add_command("shell", Shell(make_context=_make_context))

manager.run()
