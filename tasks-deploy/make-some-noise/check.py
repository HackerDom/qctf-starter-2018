FLAG = 'QCTF{vMXnTGBgntq5vjpaH3Ad}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)