#!/usr/bin/python3

import sys
import os
import string
import random
import json
import base64

SEED = 65243
FLAG_TEMPLATE = 'QCTF{{CATDOG_{}}}'
FLAG_SUFFIX_LENGTH = 8
FILENAME_LENGTH = 10

def generate_flag(rand):
    suffix = ''.join([rand.choice(string.ascii_uppercase) for _ in range(FLAG_SUFFIX_LENGTH)])
    return FLAG_TEMPLATE.format(suffix)

def generate_random_name(rand):
    return ''.join([rand.choice(string.ascii_lowercase) for _ in range(FILENAME_LENGTH)])

def main():
    if len(sys.argv) < 2:
        print("Usage: {} number-of-teams".format(sys.argv[0]))
        return

    n = int(sys.argv[1])
    rand = random.Random(SEED)

    used_flags = set()
    used_filenames = set()

    result = []
    for i in range(n):
        flag = None
        while flag is None or flag in used_flags:
            flag = generate_flag(rand)
        filename = None
        while filename is None or filename in used_filenames:
            filename = generate_random_name(rand) + '.png'
        result.append({'flag': flag, 'filename': filename})

    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
