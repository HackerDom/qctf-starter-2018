FLAG = 'QCTF{YDIWwDJUbrtqhvDHnmuT}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)
