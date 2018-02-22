import faker

from email_confirmations.models import User, Note


DEFAULT_NOTE_COUNT = 15


fake = faker.Faker()


def generate_user(username=None):
    if username is None:
        username = fake.user_name()
    password = fake.password()
    email = fake.safe_email()
    return User.with_password(
        username=username,
        email=email,
        password=password,
        confirmed=True)


def generate_note(author):
    return Note(
        title=fake.text(max_nb_chars=70),
        content=fake.text(max_nb_chars=300),
        author=author)


def generate_dummy_with_notes(username=None, note_count=DEFAULT_NOTE_COUNT):
    dummy = generate_user(username=username)
    notes = [
        generate_note(author=dummy)
        for _ in range(note_count)]
    return dummy, notes
