import json
import sqlite3
import click
from flask import g
from app import app

DATABASE = app.config['DATABASE_FILE']

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=()):
    cur = get_db().execute(query, args)
    try:
        return cur.fetchall()
    finally:
        cur.close()

def query_db_and_commit(query, args=()):
    get_db().execute(query, args).close()
    get_db().commit()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def init_users(users_file):
    with open(users_file) as f:
        users = json.load(f)
    db = get_db()
    for user in users:
        db.execute('insert into users (login, password, directory) values (?, ?, ?)', [user['login'], user['password'], user['directory']])
    db.commit()

@app.cli.command('initdb')
@click.option('--users')
def initdb_command(users):
    """Initializes the database."""
    init_db()
    init_users(users)
    print('Initialized the database.')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
