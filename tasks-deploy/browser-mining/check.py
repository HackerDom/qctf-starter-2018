FLAG = 'QCTF{SCfXDQCTeQi7tc4VHdAP}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)