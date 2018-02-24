#!/usr/bin/env python3

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from handlers import *
from config import aplication_config
from db import DbHandler

import sys


class MainApplication(Application):
    def __init__(self, flag, port):
        handlers = [
            (r"/", IndexHandler),
            (r"/shop", ShopHandler, {"flag":flag}),
            (r"/task", TaskHandler),
            (r"/login", LoginHandler)
        ]
        Application.__init__(self, handlers, **aplication_config)
        print('Inited on http://localhost:{}'.format(port))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: ./server.py <flag> <port>')
    else:
        flag, port = sys.argv[1], int(sys.argv[2])
        app = MainApplication(flag, port)
        server = HTTPServer(app, xheaders=True)
        server.bind(port)
        server.start(0)  # forks one process per cpu
        IOLoop.current().start()
