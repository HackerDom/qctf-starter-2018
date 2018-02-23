import os
import sys
import random
import shutil

from hashlib import md5


SEED = 881488

TEAM_COUNT = 400
TOKEN_SIZE = 20

TASK_ID = 'eujiyqlgrginkij'

DIR_PREFIX     = '/tmp/'
TASK_FILENAME  = 'teams'


rand = random.Random()
rand.seed(SEED)


def list2str(array):
    str = ''
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


def generate_generate(filename, statement, tokens):
    tokens_string = list2str(tokens)

    with open(filename, 'w') as f:
        f.write('''#!/usr/bin/env python3

TITLE = "TODO ВМ"

STATEMENT = \'\'\'
{}
\'\'\'

task_ids = [{}]


def generate(context):
    participant = context['participant']

    task_id = task_ids[participant.id % len(task_ids)]

    return TaskStatement(TITLE, STATEMENT.format(task_id))'''.format(statement, tokens_string))


def randstring():
    inner = ''.join([chr(rand.choice(list(range(255)))) for _ in range(32)])
    hash = md5()
    hash.update(inner.encode())
    return hash.hexdigest()


def generate_dirs():
    flags  = []
    tokens = []

    try:
        os.mkdir(os.path.join(DIR_PREFIX, TASK_FILENAME))
    except FileExistsError:
        pass
    
    for _ in range(TEAM_COUNT):
        flag  = 'QCTF{' +  randstring()[:-2] + '}'
        token = randstring()
        
        teamdir = os.path.join(DIR_PREFIX, TASK_FILENAME, token)

        try:
            os.mkdir(teamdir)
        except FileExistsError:
            pass
        
        print('Team token: ' + token)
        os.system('python3 task_gen.py {}'.format(flag))
        print()

        shutil.copy('vm.py', teamdir)
        shutil.copy('memory', teamdir)

        flags.append(flag)
        tokens.append(token)

    return flags, tokens



def main():
    flags, tokens = generate_dirs()

    statement = '''TODO Какое-то описание

Виртуальная машина: [vm.py](/static/files/%s/teams/{0}/vm.py)
Память для ВМ: [memory](/static/files/%s/teams/{0}/memory)''' % (TASK_ID, TASK_ID)

    generate_check('./check.py', flags)
    generate_generate('./generate.py', statement, tokens)


if __name__ == '__main__':
    main()