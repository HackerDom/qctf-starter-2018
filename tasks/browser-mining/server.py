#!/usr/bin/env python3

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from handlers import *
from config import aplication_config, db_config
from db import DbHandler

import sys


class MainApplication(Application):
    def __init__(self, flag, port):
        db = DbHandler(db_config)
        handlers = [
            (r"/", IndexHandler, {"db":db}),
            (r"/shop", ShopHandler, {"db":db, "flag":flag}),
            (r"/task", TaskHandler, {"db":db}),
            (r"/login", LoginHandler, {"db":db}) 
        ]
        Application.__init__(self, handlers, **aplication_config)
        print('Inited on http://localhost:{}'.format(port))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: ./server.py <flag> <port>')
    else:
        flag, port = sys.argv[1], int(sys.argv[2])
        app = HTTPServer(MainApplication(flag, port))
        app.listen(port)
        IOLoop.instance().start()