import argparse
import random
import json
import string

FLAG_PREFIX = 'QCTF{1o0k_aT_tH3_b0dy_'
ALPHABET = string.ascii_lowercase + string.digits


def parse_args():
    parser = argparse.ArgumentParser(prog='generate_flags.py', description='Generates flags for teams')
    parser.add_argument('count', type=int, help='Teams number')
    parser.add_argument('seed', type=int, help='Random generator seed')
    parser.add_argument('id_length', type=int, nargs='?', help='Team id length. Default is 10', default=8)
    parser.add_argument('flag_length', type=int, nargs='?', help='Flag random part length. Default is 10', default=10)
    return parser.parse_args()


def generate_string(length):
    return ''.join([random.choice(ALPHABET) for _ in range(length)])


def main():
    args = parse_args()
    flags = []
    random.seed(args.seed)
    while len(flags) < args.count:
        team_id = generate_string(args.id_length)
        suffix = generate_string(args.flag_length)
        flag = FLAG_PREFIX + suffix + '}'
        if len(list(filter(lambda dic: team_id == dic['team_id'] or flag == dic['flag'], flags))) == 0:
            flags.append({'team_id': team_id, 'flag': flag})

    with open('flags.json', 'w') as file:
        json.dump(flags, file, indent=4)


if __name__ == '__main__':
    main()
