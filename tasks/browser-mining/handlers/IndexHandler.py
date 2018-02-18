from tornado.web import RequestHandler
from tornado import gen


class IndexHandler(RequestHandler):
    def initialize(self, db):
        self.db = db
    
    @gen.coroutine
    def get(self):
        user = self.get_secure_cookie("user").decode()        
        if user:
            balance = yield self.db.get_balance(user)
            self.render('index.html', balance=balance)
        else:
            self.redirect("/login")