from tornado.web import RequestHandler
from tornado import gen
from json import dumps, loads
from random import randint


class TaskHandler(RequestHandler):
    def initialize(self, db):
        self.db = db

    @gen.coroutine
    def post(self):
        user = self.get_secure_cookie("user").decode()
        result = int(loads(self.request.body.decode()).get('result', '0'))
        new_task = self.generate_task()
        balance = yield self.db.update_score(user, result, new_task)
        self.write(dumps({
            "task" : new_task,
            "balance" : balance
        }))

    def generate_task(self):
        return randint(2**17, 2**24)