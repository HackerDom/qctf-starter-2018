#!/usr/bin/env python3

from random import choice, seed
from string import digits, ascii_letters
import os.path


ALPHA = digits + ascii_letters

if __name__ == "__main__":
    seed(0x80085)
    ids = [''.join(choice(ALPHA) for _ in range(20)) for x in range(400)]
    flags = ['QCTF{{g00D_N0isss3_{}}}'.format(''.join(choice(ALPHA) for _ in range(6))) for x in range(400)]
    with open(os.path.join('flask','ids_and_flags.py'), 'w') as f:
        f.write('ids = {}\n'.format(repr(ids)))
        f.write('flags = {}'.format(repr(flags)))