import argparse
import secrets
import json

FLAG_PREFIX = 'QCTF_1o0k_aT_tH3_b0dy_'


def parse_args():
    parser = argparse.ArgumentParser(prog='generate_flags.py', description='Generates flags for teams')
    parser.add_argument('count', type=int, help='Teams number')
    parser.add_argument('id_length', type=int, nargs='?', help='Team id length. Default is 10', default=8)
    parser.add_argument('flag_length', type=int, nargs='?', help='Flag random part length. Default is 10', default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    flags = {}
    while len(flags) < args.count:
        team_id = secrets.token_hex(args.id_length)
        suffix = secrets.token_hex(args.flag_length)
        flag = FLAG_PREFIX + suffix
        if team_id not in flags.keys() and flag not in flags.values():
            flags[team_id] = flag

    with open('flags.json', 'w') as file:
        json.dump(flags, file, indent=4)


if __name__ == '__main__':
    main()
