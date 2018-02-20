#!/usr/bin/python3

import sys
import os
import string
import random
import json
import base64

root = os.path.dirname(__file__)
sys.path.append(root + "/flask/app")
sys.path.append(root + "/flask")

from cipher import CipherProvider
import config

FLAG_PREFIX = 'QCTF_DONT_USE_CUSTOM_CIPHERS_'
FLAG_SUFFIX_LENGTH = 10

def generate_flag(rand):
    suffix = ''.join([rand.choice(string.ascii_uppercase) for _ in range(FLAG_SUFFIX_LENGTH)])
    return FLAG_PREFIX + suffix

def main():
    if len(sys.argv) < 2:
        print("Usage: {} number-of-teams".format(sys.argv[0]))
        return

    n = int(sys.argv[1])
    seed = config.CIPHER_GLOBAL_SEED
    key_len = config.CIPHER_KEY_LEN

    rand = random.Random(seed + 100)
    cipher = CipherProvider.get_cipher(seed, key_len)

    result = []
    for i in range(n):
        flag = generate_flag(rand)
        encryption = cipher.encrypt(flag.encode())
        result.append({'flag': flag, 'data': base64.b64encode(encryption).decode()})

    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
