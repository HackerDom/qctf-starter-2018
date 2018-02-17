import sqlite3
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

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
