FLAG = 'QCTF{451b3208300ba3f7ecc115e84f2eb3d5}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)
