from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from handlers import *
from config import aplication_config, db_config
from db import DbHandler


class MainApplication(Application):
    def __init__(self):
        flag = "QCTF_ABCD"
        db = DbHandler(db_config)
        handlers = [
            (r"/", IndexHandler, {"db":db}),
            (r"/shop", ShopHandler, {"db":db, "flag":flag}),
            (r"/task", TaskHandler, {"db":db}),
            (r"/login", LoginHandler, {"db":db}) 
        ]
        Application.__init__(self, handlers, **aplication_config)
        print('Inited on http://localhost:8888')


if __name__ == "__main__":
    app = HTTPServer(MainApplication())
    app.listen(8888)
    IOLoop.instance().start()