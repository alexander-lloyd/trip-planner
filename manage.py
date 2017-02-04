#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# http://bootstrapmaster.com/live/genius/index.html

from app import create_app, db
from app.email import send_email
# from app.models import ...
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

print(os.getenv('FLASK_CONFIG'))
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,
                db=db,
                email=send_email)


@manager.command
def build():
    db.drop_all()
    db.create_all()
    # Fake Data
    db.session.commit()


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
