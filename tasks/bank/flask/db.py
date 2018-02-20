import random
import string


FLAG = 'QCTF{YDIWwDJUbrtqhvDHnmuT}'


def save_and_get_code(_, interest):
    if interest < 1:
        return FLAG

    return ''.join(random.choice(string.ascii_uppercase)
                   for _ in range(8))
