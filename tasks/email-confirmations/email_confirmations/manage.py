from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from email_confirmations.app import app, db
from email_confirmations.commands import (
    TruncateUsersCommand,
    GenerateFlagOwnerCommand,
    GenerateDummiesCommand
)


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('truncate_users', TruncateUsersCommand)
manager.add_command('generate_flag_owner', GenerateFlagOwnerCommand)
manager.add_command('generate_dummies', GenerateDummiesCommand)


if __name__ == '__main__':
    manager.run()
