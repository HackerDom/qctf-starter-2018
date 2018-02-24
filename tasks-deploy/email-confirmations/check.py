FLAG = 'QCTF{4e94227c6c003c0b6da6f81c9177c7e7}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)
