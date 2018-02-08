import sys
import random
import string
import hashlib

from vm import TEXT_SECTION_RANGE, HEAP_SECTION_RANGE, STACK_SECTION_RANGE, MEMORY_SIZE
from interpreter import gen_bytecode


INPUT_STR_LEN = 12
ALPHABET      = string.ascii_letters + string.digits

def gen_enc_flag(flag):
    if len(flag) != 36:
        print('[-] Invalid flag length!')
        return

    numbers = [123, 28, 72, 41, 15, 55]
    cur     = []

    for i in range(len(flag)//6):
        cur.append(''.join([chr(ord(x) ^ numbers[i]) for x in flag[i*6:i*6+6]]))

    cur[0], cur[-1] = cur[-1], cur[0]
    cur[1], cur[3]  = cur[3], cur[1]
    cur[2], cur[4]  = cur[4], cur[2]

    return ''.join(cur)


def gen_enc_str(input_str):
    if len(input_str) != INPUT_STR_LEN:
        print('[-] Invalid length of input string!')
        return

    hardcoded   = 'konata'
    to_validate = input_str[::-1] + input_str + input_str[::3]
    nvalid      = ''

    for i in range(len(to_validate)):
        nvalid += chr((ord(to_validate[i]) + 4) ^ ord(hardcoded[i % len(hardcoded)]))
    return nvalid


def gen_checks(val):
    last_hash = hashlib.sha1()
    last_hash.update(val[-5:].encode('utf-8'))
    last_hash = last_hash.hexdigest()

    mid_hash  = hashlib.md5()
    mid_hash.update(val[5:-5].encode('utf-8'))
    mid_hash = mid_hash.hexdigest()

    return {
        'first_bytes':       val[:5],
        'middle_bytes_hash': mid_hash,
        'last_bytes_hash':   last_hash
    }


def gen_task(enflag, checks):
    def insert2mem(mem, s, bytes):
        return mem[:s] + bytes + mem[s + len(bytes):]

    hp_s, hp_f = HEAP_SECTION_RANGE
    m_hp       = hp_s + (hp_f - hp_s) // 2

    r_mem    = MEMORY_SIZE * '\x00'

    bytecode = gen_bytecode()
    r_mem = insert2mem(r_mem, 0, bytecode)
    r_mem = insert2mem(r_mem, m_hp,     checks['first_bytes'])
    r_mem = insert2mem(r_mem, m_hp+100, checks['middle_bytes_hash'])
    r_mem = insert2mem(r_mem, m_hp+200, checks['last_bytes_hash'])
    r_mem = insert2mem(r_mem, m_hp+300, enflag)

    # print(repr(r_mem))

    with open('memory', 'wb') as mem:
        mem.write(r_mem.encode())


def validating_algo(inp, checks):
    val = gen_enc_str(inp)


def gen_input(flag):
    hs = hashlib.sha1()
    md = hashlib.md5()
    hs.update(flag.encode())
    md.update(hs.hexdigest().encode())
    return md.hexdigest()[:INPUT_STR_LEN]


def main():
    if len(sys.argv) != 2:
        print('Usage: gen.py <flag>')
        return
    flag = sys.argv[1]
    inp  = gen_input(flag)
    val  = gen_enc_str(inp)

    checks = gen_checks(val)
    enflag = gen_enc_flag(flag)

    # print(checks)
    # print(repr(enflag))

    gen_task(enflag, checks)


if __name__ == '__main__':
    main()

