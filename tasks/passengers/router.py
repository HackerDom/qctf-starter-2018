import os
import sys
import random
import string
import shutil

from hashlib import md5
from subprocess import Popen


FILE_MATCHING    = 'token_file_matching'
ROOTDIR_PREFIX   = '/passengers/'
TEAMS_DIR_PREFIX = '/passengers/teams'

TASK_ID = 'dnljlrahncokpgr'

SEED = 31337

TEAM_COUNT = 600
TOKEN_SIZE = 20


def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


class Router:
    def __init__(self):
        self.token_file_matching = {}

        self.rand = random.Random()
        self.rand.seed(SEED)

    def generate_token_file_matching(self):
        for team_id in range(TEAM_COUNT):
            token = ''
            rootdir  = ''
            for _ in range(TOKEN_SIZE):
                token += self.rand.choice(list(string.ascii_letters + string.digits))
                rootdir  += self.rand.choice(list(string.ascii_letters))
            self.token_file_matching[(team_id, token)] = rootdir

        data = [None] * TEAM_COUNT
        for k, v in self.token_file_matching.items():
            data[k[0]] = (k[1], v)
        with open(os.path.join(ROOTDIR_PREFIX, FILE_MATCHING), 'w') as f:
            f.write('\n'.join(['{}:{}:{}'.format(i, pair[0], pair[1]) for i, pair in enumerate(data)]))

    def generate_dirs(self):
        try:
            shutil.rmtree(TEAMS_DIR_PREFIX)
        except FileNotFoundError:
            pass
        os.mkdir(TEAMS_DIR_PREFIX)

        flags1 = [None] * TEAM_COUNT
        flags2 = [None] * TEAM_COUNT
        tokens = [None] * TEAM_COUNT

        for key, rootdir in self.token_file_matching.items():
            team_id = key[0]
            token   = key[1]

            os.makedirs(os.path.join(TEAMS_DIR_PREFIX, rootdir))
            shutil.copytree(os.path.join(get_current_dir(), 'service'), os.path.join(TEAMS_DIR_PREFIX, rootdir, 'service'))

            for flag_index, flagarray in zip(['1', '2'], [flags1, flags2]):
                with open(os.path.join(TEAMS_DIR_PREFIX, rootdir, 'service', 'flag' + flag_index), 'w') as f:
                    hash = md5()
                    hash.update(''.join([chr(self.rand.choice(list(range(255)))) for _ in range(32)]).encode())
                    flag = 'QCTF{' + hash.hexdigest() + '}'

                    f.write(flag)
                    flagarray[team_id] = flag
                    tokens[team_id]    = (token, rootdir)

        return tokens, flags1, flags2


    def init_token_file_matching(self):
        with open(os.path.join(ROOTDIR_PREFIX, FILE_MATCHING), 'r') as f:
            token_matching = {}
            for line in f.readlines():
                team_id, token, rootdir = line[:-1].split(':')
                self.token_file_matching[(team_id, token)] = rootdir
                token_matching[token] = rootdir
        return token_matching


def main():
    os.chdir(TEAMS_DIR_PREFIX)

    router = Router()
    token_matching = router.init_token_file_matching()

    token = input('[*] Team token: ')

    if token not in token_matching:
        print('[-] Incorrect token.')
        return

    rootdir = token_matching[token]
    os.chdir(os.path.join(TEAMS_DIR_PREFIX, rootdir, 'service'))

    p = Popen(['su', 'passengers', '-c', './main {}'.format(token)])
    p.communicate()


def list2str(array, inner_list=False):
    str = ''
    if inner_list:
        for elem in array:
            str += '["{}", "{}"], '.format(elem[0], elem[1])
    else:
        for elem in array:
            str += '"{}", '.format(elem)
    return str[:-2]

def generate_check(filename, flags):
    flags_string = list2str(flags)

    with open(filename, 'w') as f:
        f.write('''#!/usr/bin/env python3


flags = [{}]

def check(attempt, context):
    if attempt.answer == flags[attempt.participant.id % len(flags)]:
        return Checked(True)
    if attempt.answer in flags:
        return CheckedPlagiarist(False, flags.index(attempt.answer))
    return Checked(False)'''.format(flags_string))


def generate_generate(filename, title, statement, tokens):
    tokens_string = list2str(tokens, True)

    with open(filename, 'w') as f:
        f.write('''#!/usr/bin/env python3

TITLE = "{}"

STATEMENT = \'\'\'
{}
\'\'\'

task_ids = [{}]


def generate(context):
    participant = context['participant']

    task_id = task_ids[participant.id % len(task_ids)]

    return TaskStatement(TITLE, STATEMENT.format(task_id[1], task_id[0]))'''.format(title, statement, tokens_string))


def prepare():
    route = Router()
    route.generate_token_file_matching()

    tokens, flags1, flags2 = route.generate_dirs()

    try:
        os.mkdir(os.path.join(get_current_dir(), '1'))
        os.mkdir(os.path.join(get_current_dir(), '2'))
    except FileExistsError:
        pass

    statement ='''
НЕСА проводит очередной набор исследователей в свою космическую команду. На текущий момент уже готова система для подачи заявок, и разработчики из НЕСА рады поделиться её прототипом!
Для того, чтобы зайти на сервис, необходимо указать токен вашей команды.

Прототип: [main](/static/files/%s/{0}/service/main)
Исходный код: [main.c](/static/files/%s/{0}/service/main.c)
Токен: {1}
''' % (TASK_ID, TASK_ID)

    generate_check('./1/check.py', flags1)
    generate_generate('./1/generate.py', 'Пассажиры. Часть первая', statement, tokens)

    generate_check('./2/check.py', flags2)
    generate_generate('./2/generate.py', 'Пассажиры. Часть вторая', statement, tokens)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'prepare':
            prepare()
    else:
        main()
