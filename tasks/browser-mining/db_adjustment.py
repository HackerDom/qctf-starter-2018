from config import db_config
from tornado_mysql import connect
from getpass import getpass
from tornado import gen, ioloop

@gen.coroutine
def db_adj(root, passwd):
    #############################################################
    # Если этот блок не сработал, то нужно создать пользователя #
    # вручную и, закоментировав блок, запустить скрипт ещё раз  #
    #############################################################
    conn = yield connect(host=db_config['host'], charset=db_config['charset'], user=root, passwd=passwd)
    cur = conn.cursor()
    yield cur.execute('DROP USER IF EXISTS %s@%s', (db_config['user'], db_config['host']))
    yield cur.execute('CREATE USER %s@%s IDENTIFIED BY %s', (db_config['user'], db_config['host'], db_config['passwd']))
    yield cur.execute('GRANT ALL PRIVILEGES ON * . * TO %s@%s', (db_config['user'], db_config['host']))
    yield cur.execute('FLUSH PRIVILEGES')
    cur.close()
    conn.commit()
    conn.close()
    print('USER CREATED!')
    #############################################################

    conn = yield connect(host=db_config['host'], charset=db_config['charset'], user=db_config['user'], passwd=db_config['passwd'])
    cur = conn.cursor()
    yield cur.execute('DROP DATABASE IF EXISTS {}'.format(db_config['db']))
    yield cur.execute('CREATE DATABASE {}'.format(db_config['db']))
    cur.close()
    conn.commit()
    conn.close()
    print('DATABASE CREATED!')

    conn = yield connect(**db_config)
    cur = conn.cursor()
    yield cur.execute('CREATE TABLE users(login VARCHAR(20) PRIMARY KEY, password VARCHAR(65), balance INT, task BIGINT)')
    cur.close()
    conn.commit()
    conn.close()
    print('TABLES CREATED!')

    print('Done!')

if __name__ == "__main__":
    root = input('Your root login for mysql: ')
    passwd = getpass('Your root password: ')

    ioloop.IOLoop.current().run_sync(lambda: db_adj(root, passwd))