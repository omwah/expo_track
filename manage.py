#!/usr/bin/env python

from flask.ext.script import Command, Manager, Shell

from expo_track import app

manager = Manager(app)

class sync_db(Command):
    """
    Initializes the database tables.
    """
    def run(self):
        from expo_track import db
        db.drop_all()
        db.create_all()
        db.session.commit()


class fixed_shell(Shell):
    """
    Runs a Python shell inside Flask application context.
    """
    def run(self, no_ipython):
        context = self.get_context()
        if not no_ipython:
            try:
                from IPython.frontend.terminal.embed import InteractiveShellEmbed
                sh = InteractiveShellEmbedbanner1=self.banner
                sh(global_ns=dict(), local_ns=context)
            except ImportError:
                pass
        from code import interact
        interact(banner=self.banner, local=context)

manager.add_command('syncdb', sync_db())
manager._commands['shell'] = fixed_shell()
manager.run()
