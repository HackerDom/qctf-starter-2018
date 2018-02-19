import os
import random
import time
import string
from collections import deque, namedtuple
from itertools import zip_longest

import numpy as np
from PIL import Image
from flask import Flask, abort, request, jsonify
from keras.models import load_model


PASSWORD = [random.choice(string.digits) for _ in range(10)]
FLAG = 'QCTF_KEK'

assert len(PASSWORD) == 10


# Source: cnn.h5 from https://github.com/EN10/KerasMNIST
mnist_cnn = load_model(os.path.join(os.path.dirname(__file__), 'mnist_cnn.h5'))

MNIST_WH = 28
MNIST_CONTENT_WH = 20


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 ** 2

MAX_IMAGE_WH = 3000


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/submit_image', methods=['POST'])
def submit_image():
    start_time = time.time()

    img = Image.open(request.files['image'])
    if img.width > MAX_IMAGE_WH or img.height > MAX_IMAGE_WH:
        return abort(400)
    img = img.convert('L')

    correct = True
    for actual, expected in zip_longest(find_digits(img), PASSWORD):
        if actual != expected:
            correct = False
            break

    if correct:
        status = 'Верный пароль! Флаг: <b>{}</b>'.format(FLAG)
    else:
        status = 'Неверный пароль'
    elapsed_time = time.time() - start_time
    status += ' ({} мс)'.format(round(elapsed_time * 1000))  # dbg
    return jsonify({
        'status': status,
        'elapsed_ms': round(elapsed_time * 1000),
    })


Rectangle = namedtuple('Rectangle', ['x1', 'y1', 'x2', 'y2'])


def find_digits(img):
    pixels = img.load()
    visited = np.zeros(img.size, dtype=np.bool)
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] != 0 and not visited[x, y]:
                rect = traverse_rect(img, pixels, visited, x, y)
                rect_w = rect.x2 - rect.x1
                rect_h = rect.y2 - rect.y1

                scale = max(rect_w / MNIST_CONTENT_WH,
                            rect_h / MNIST_CONTENT_WH)
                digit = img.crop(rect).resize((round(rect_w / scale),
                                               round(rect_h / scale)))
                wrapper = Image.new('L', (MNIST_WH, MNIST_WH))
                wrapper.paste(digit, ((wrapper.width - digit.width) // 2,
                                      (wrapper.height - digit.height) // 2))
                w_pixels = np.array(wrapper).reshape(1, MNIST_WH, MNIST_WH, 1)
                X = (w_pixels - w_pixels.min()) / (w_pixels.max() - w_pixels.min())

                digit = np.argmax(mnist_cnn.predict(X)[0])
                yield str(digit)


NEIGH_DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def traverse_rect(img, pixels, visited, x0, y0):
    order = deque()
    order.append((x0, y0))
    visited[x0, y0] = True
    rect = Rectangle(x0, y0, x0 + 1, y0 + 1)

    while len(order) > 0:
        x, y = order.popleft()

        for dx, dy in NEIGH_DIRECTIONS:
            new_x = x + dx
            new_y = y + dy
            if not (0 <= new_x < img.width and 0 <= new_y < img.height):
                continue

            if pixels[new_x, new_y] != 0 and not visited[new_x, new_y]:
                order.append((new_x, new_y))
                visited[new_x, new_y] = True
                rect = Rectangle(min(rect.x1, new_x), min(rect.y1, new_y),
                                 max(rect.x2, new_x + 1), max(rect.y2, new_y + 1))
    return rect
