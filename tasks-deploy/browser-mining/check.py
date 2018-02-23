FLAG = 'QCTF{Her3_C0m3s_Th3_m0neY}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)