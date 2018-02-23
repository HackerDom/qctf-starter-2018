from tornado.web import RequestHandler
from tornado import gen
from db import DbHandler

class IndexHandler(RequestHandler):
    def initialize(self):
        self.db = DbHandler.get_db()
    
    @gen.coroutine
    def get(self):
        user = self.get_secure_cookie("user")
        if user:
            balance = yield self.db.get_balance(user.decode())
            self.render('index.html', balance=balance)
        else:
            self.redirect("/login")
