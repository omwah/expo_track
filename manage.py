#!/usr/bin/env python

import os

from flask.ext.script import Command, Manager, Shell

from expo_track import app, db, models

manager = Manager(app)

@manager.command
def syncdb():
    'Resets the database tables.'

    if not os.path.exists(app.config['INSTANCE_DIR']):
        os.makedirs(app.config['INSTANCE_DIR'])

    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def initdb():
    'Resets database tables and initializes with initial data'

    syncdb()

    admin_person = models.Person(given_name='Admin')
    admin_user = models.User(name='admin',
                             password='123456',
                             person=admin_person)
    db.session.add(admin_user)
    db.session.commit()

def _make_context():
    return dict(app=app, db=db, models=models)

manager.add_command("shell", Shell(make_context=_make_context))

manager.run()
