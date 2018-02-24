from flask_script import Command, Option

from email_confirmations.models import db, User, Note
from email_confirmations.generation import generate_dummy_with_notes


class TruncateUsersCommand(Command):
    def run(self):
        # Postgres-specific. Contestants shouldn't need to guess the first id
        db.session.execute('TRUNCATE TABLE {} RESTART IDENTITY CASCADE'
                           .format(User.__tablename__))
        db.session.commit()


class GenerateFlagOwnerCommand(Command):
    option_list = (
        Option('flag'),
    )

    def run(self, flag):
        user, notes = generate_dummy_with_notes(username='admin')
        flag_note = Note(
            title='Hope no one sees this note',
            content=flag,
            author=user)
        db.session.add(user)
        db.session.add_all(notes)
        db.session.add(flag_note)
        db.session.commit()


class GenerateDummiesCommand(Command):
    option_list = (
        Option('dummy_count', type=int),
    )

    def run(self, dummy_count):
        if dummy_count < 0:
            raise ValueError('Dummy count should be non-negative, got {}'
                             .format(dummy_count))

        for _ in range(dummy_count):
            dummy, notes = generate_dummy_with_notes()
            db.session.add(dummy)
            db.session.add_all(notes)
        db.session.commit()
