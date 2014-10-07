# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from loctube import create_app
from loctube.extensions import db
from loctube.user import User, UserDetail, ADMIN, ACTIVE
from loctube.utils import MALE


app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            password=u'123456',
            role_code=ADMIN,
            status_code=ACTIVE,
            user_detail=UserDetail(
                sex_code=MALE,
                age=10,
                url=u'http://loctube.com',
                deposit=100.00,
                location=u'Chicago',
                bio=u'Mehmet Vergili'))
    db.session.add(admin)
    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
