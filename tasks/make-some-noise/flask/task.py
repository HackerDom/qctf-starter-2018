#!/usr/bin/env python3

import logging
from random import choice, randint
from math import sqrt
from sys import argv
from flask import Flask
from ids_and_flags import ids, flags


def get_noised_flag(flag):
    n = 35
    noise = list(range(-n, n+1))
    return [add_noise(x, noise) for x in map(ord,flag)]

def add_noise(x, noise):
    return x + choice(noise)

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)


@app.route('/<team_id>')
def hello(team_id):
    try:
        id = ids.index(team_id)
        return str(get_noised_flag(flags[id]))
    except Exception:
        return "Wrong team id!"

@app.route('/')
def index():
    return "Wrong team id!"

if __name__ == "__main__":
    app.run()
