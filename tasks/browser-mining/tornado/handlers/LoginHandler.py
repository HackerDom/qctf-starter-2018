from tornado.web import RequestHandler
from tornado import gen
from db import DbHandler

class LoginHandler(RequestHandler):
    def initialize(self):
        self.db = DbHandler.get_db()
    
    def get(self):
        self.clear_cookie('user')
        self.render('login.html')

    @gen.coroutine
    def post(self):
        login = self.get_argument("login", '', strip=True)
        password = self.get_argument("password", '', strip=True)
        if not (login and password):
            raise Exception("Empty login or password")

        res = yield self.db.login(login, password)
        if res:
            self.set_secure_cookie("user", login)
            self.redirect("/")
        else:
            self.redirect("/login")
