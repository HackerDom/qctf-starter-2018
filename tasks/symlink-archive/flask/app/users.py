import random
import string

from flask_login import UserMixin
from app.db import query_db, query_db_and_commit
from app import app

class UserProvider:
    @staticmethod
    def find_user(login):
        result = query_db('select password, directory from users where login=?', [login])
        if len(result) == 0:
            return None
        return User(login, result[0][0], result[0][1])
    
    @staticmethod
    def create_user(login, password):
        if query_db('select count(*) from users where login=?', [login])[0][0] > 0:
            return None
        if login in app.config['FAKE_USERS']:
            return None
        directory = [random.choice(string.ascii_lowercase) for _ in range(10)]
        query_db_and_commit('insert into users (login, password, directory) values (?, ?, ?)', [login, password, directory])
        return User(login, password, directory)
        

class User(UserMixin):
    def __init__(self, login, password, directory):
        self.login = login
        self.password = password
        self.directory = directory

    def get_id(self):
        return self.login

    @staticmethod
    def get(user_id):
        result = query_db('select password, directory from users where login=?', [user_id])
        if len(result) != 1:
            return None
        return User(user_id, result[0][0], result[0][1])
