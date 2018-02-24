FLAG = 'QCTF{755982704c899da19a935786649281b6}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)
