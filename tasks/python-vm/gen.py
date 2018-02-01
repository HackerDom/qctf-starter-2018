import random
import string
import hashlib


INPUT_STR_LEN = 12
ALPHABET      = string.ascii_letters + string.digits

def generate_deflag(flag):
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


def generate_valid_str(input_str):
    if len(input_str) != INPUT_STR_LEN:
        print('[-] Invalid length of input string!')
        return

    hardcoded   = 'konata'
    to_validate = input_str[::-1] + input_str + input_str[::3]
    nvalid      = ''

    for i in range(len(to_validate)):
        nvalid += chr((ord(to_validate[i]) + 4) ^ ord(hardcoded[i % len(hardcoded)]))

    return nvalid


def generate_checks(val):
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


def generate_task(val, deflag):
    pass


def validating_algo(inp, checks):
    val = generate_valid_str(inp)


def main():
    inp = 'ne4IrUcD1V8U'
    val = generate_valid_str(inp)
    checks = generate_checks(val)
    deflag = generate_deflag('QCTF{some_text_here!!this_is_a_flag}')


if __name__ == '__main__':
    main()

