import logging
import os
import re
import time
from collections import deque, namedtuple
from itertools import zip_longest

import numpy as np
from PIL import Image
from flask import Flask, abort, request, jsonify
from keras.models import load_model


PASSWORD = '3081435172'
FLAG = 'QCTF{VmRDwFKNzSGoBrWUJyGu}'

assert re.fullmatch(r'\d{10}', PASSWORD) is not None


# Source: cnn.h5 from https://github.com/EN10/KerasMNIST
model_path = os.path.join(os.path.dirname(__file__), 'mnist_cnn.h5')
mnist_cnn = load_model(model_path)

MNIST_WH = 28
MNIST_CONTENT_WH = 20


app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)

app.config['MAX_CONTENT_LENGTH'] = 1024 ** 2

CRITICAL_IMAGE_WH = 3000
MAX_IMAGE_W, MAX_IMAGE_H = 1000, 500


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/submit_image', methods=['POST'])
def submit_image():
    start_time = time.time()

    img = Image.open(request.files['image'])
    if max(img.width, img.height) > CRITICAL_IMAGE_WH:
        abort(400)

    scale = min(MAX_IMAGE_W / img.width, MAX_IMAGE_H / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)))
    img = img.convert('L')

    recognized = ''
    correct = True
    for actual, expected in zip_longest(find_digits(img), PASSWORD):
        if actual is not None:
            recognized += actual
        if actual != expected:
            correct = False
            break
    app.logger.info('recognized = "{}"  correct = {}'.format(recognized, correct))

    if correct:
        status = 'Верный пароль! Флаг: <span class="flag">{}</span>'.format(FLAG)
    else:
        status = 'Неверный пароль'
    elapsed_time = time.time() - start_time
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
            if visited[x, y] or pixels[x, y] == 0:
                continue

            rect = traverse_rect(img, pixels, visited, x, y)
            rect_w = rect.x2 - rect.x1
            rect_h = rect.y2 - rect.y1

            scale = min(MNIST_CONTENT_WH / rect_w, MNIST_CONTENT_WH / rect_h)
            digit = img.crop(rect)
            digit = digit.resize((round(rect_w * scale), round(rect_h * scale)))
            wrapper = Image.new('L', (MNIST_WH, MNIST_WH))
            wrapper.paste(digit, ((wrapper.width - digit.width) // 2,
                                  (wrapper.height - digit.height) // 2))
            w_pixels = np.array(wrapper).reshape(1, MNIST_WH, MNIST_WH, 1)
            X = (w_pixels - w_pixels.min()) / (w_pixels.max() - w_pixels.min())

            digit = np.argmax(mnist_cnn.predict(X)[0])
            yield str(digit)


NEIGH_DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def traverse_rect(img, pixels, visited, x0, y0):
    width, height = img.size

    order = deque()
    order.append((x0, y0))
    visited[x0, y0] = True
    min_x = x0
    min_y = y0
    max_x = x0 + 1
    max_y = y0 + 1

    while len(order) > 0:
        x, y = order.popleft()

        for dx, dy in NEIGH_DIRECTIONS:
            new_x = x + dx
            new_y = y + dy
            if (
                not (0 <= new_x < width and 0 <= new_y < height) or
                visited[new_x, new_y] or
                pixels[new_x, new_y] == 0
            ):
                continue

            order.append((new_x, new_y))
            visited[new_x, new_y] = True

            min_x = min(min_x, new_x)
            min_y = min(min_y, new_y)
            max_x = max(max_x, new_x + 1)
            max_y = max(max_y, new_y + 1)
    return Rectangle(min_x, min_y, max_x, max_y)
