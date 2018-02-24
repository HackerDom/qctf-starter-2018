from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from bulls_and_cows.app import app, db
from bulls_and_cows.commands import TruncateUsersCommand


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('truncate_users', TruncateUsersCommand)


if __name__ == '__main__':
    manager.run()
