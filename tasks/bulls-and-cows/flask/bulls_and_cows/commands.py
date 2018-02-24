from flask_script import Command

from bulls_and_cows.models import db, User


class TruncateUsersCommand(Command):
    def run(self):
        # Postgres-specific
        db.session.execute('TRUNCATE TABLE {} RESTART IDENTITY CASCADE'
                           .format(User.__tablename__))
        db.session.commit()
