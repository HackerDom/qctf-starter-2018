#!/usr/bin/env python3

import logging
import numpy as np
from flask import Flask, abort
from ids_and_flags import ids, flags


def get_noised_flag(flag):
    with_noise = [np.random.normal(x, 2, 1)[0] for x in map(ord, flag)]
    return ''.join(list(map(lambda num: chr(int(round(num))), with_noise)))


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)


@app.route('/<team_id>')
def hello(team_id):
    try:
        id = ids.index(team_id)
        return str(get_noised_flag(flags[id]))
    except ValueError:
        return "Wrong team id!"
    except Exception as e:
        app.logger.exception(e)
        abort(500)


@app.route('/')
def index():
    return "Wrong team id!"


if __name__ == "__main__":
    app.run()
