from tornado.web import RequestHandler
from tornado import gen
from json import dumps

class ShopHandler(RequestHandler):
    def initialize(self, db, flag):
        self.db = db
        self.flag = flag
    
    @gen.coroutine
    def get(self):
        user = self.get_secure_cookie("user").decode()        
        if user:
            balance = yield self.db.get_balance(user)
            self.render("shop.html", balance=balance)
        else:
            self.redirect("/login")  

    @gen.coroutine
    def post(self):
        user = self.get_secure_cookie("user").decode()
        flag, balance = yield self.db.get_flag(user)
        if flag:
            self.write(dumps({
                "flag" : self.flag,
                "balance" : balance
            }))
        else:
            self.write(dumps({
                "error" : "Недостаточно монет",
                "balance" : balance
            }))