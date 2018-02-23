from tornado import gen
from tornado_mysql import pools
from gmpy2 import next_prime
from config import db_config

class DbHandler():
    def __init__(self, config):
        self.POOL = pools.Pool(
            config,
            max_idle_connections=1,
            max_recycle_sec=3
        )
        self.LOGIN = "SELECT * FROM users WHERE login=%s LIMIT 1"
        self.REGISTER = "INSERT INTO users(login, password, balance, task) VALUES (%s, %s, 0, 0)"
        self.UPDATE_SCORE = "UPDATE users SET balance=%s, task=%s WHERE login=%s"
    
    @staticmethod
    def get_db():
        db = getattr(DbHandler, '_database', None)
        if db is None:
            db = DbHandler._database = DbHandler(db_config)
        return db

    @gen.coroutine
    def login(self, login, password):
        cur = yield self.POOL.execute(self.LOGIN, (login,))
        founded = cur.fetchall()
        if not founded:
            yield self.POOL.execute(self.REGISTER, (login, password))
            founded = (login, password, 0)
        else:
            founded = founded[0]
        return founded[1] == password, founded[2]

    @gen.coroutine
    def update_score(self, login, result, new_task):
        cur = yield self.POOL.execute(self.LOGIN, (login,))
        res = cur.fetchall()[0]
        new_balance, task = res[2:]
        if next_prime(task) == result:
            new_balance += 1
        yield self.POOL.execute(self.UPDATE_SCORE, (new_balance, new_task, login))
        return new_balance

    @gen.coroutine
    def get_flag(self, login):
        TASK_VALUE = 10000
        cur = yield self.POOL.execute(self.LOGIN, (login,))
        res = cur.fetchall()[0]
        balance, task = res[2:]
        if balance >= TASK_VALUE:
            balance = balance-TASK_VALUE
            yield self.POOL.execute(self.UPDATE_SCORE, (balance, task, login))
            return True, balance
        else:
            return False, balance

    @gen.coroutine
    def get_balance(self, login):
        cur = yield self.POOL.execute(self.LOGIN, (login,))
        return cur.fetchall()[0][2]
        
