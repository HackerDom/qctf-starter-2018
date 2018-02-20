FLAG = 'QCTF{VmRDwFKNzSGoBrWUJyGu}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)
