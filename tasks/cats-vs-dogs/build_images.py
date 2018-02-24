#!/usr/bin/python3

import os
import random
import string
import shutil
import json
from PIL import Image, ImageDraw, ImageFont

FLAGS_FILE = 'flags.txt'
OUTPUT_DIR = './output'
RAND_SEED = 453

class TextMatrixGenerator:
    def __init__(self):
        pass

    def generate_matrix_with_text(self, text, w, h):
        img = Image.new('1', (w, h), 1)
        font = ImageFont.truetype("UbuntuMono-B.ttf", h - 3)
        drawer = ImageDraw.Draw(img)
        drawer.text((3, 0), text, font=font)
      
        matrix = []
        data = img.load()
        for y in range(h):
            matrix.append([])
            for x in range(w):
                matrix[-1].append(data[x, y] == 1)
        return matrix

class CatAndDogImageGenerator:
    def __init__(self, rand):
        self.cat_files = [os.path.join('./cats', x) for x in os.listdir('./cats')]
        self.dog_files = [os.path.join('./dogs', x) for x in os.listdir('./dogs')]
        self.rand = rand

    def gen_mask_by_matrix(self, matrix, cell_size, filename):
        h = cell_size * len(matrix)
        w = cell_size * len(matrix[0])

        background_color = (255, 255, 255)
        fill_color = (0, 0, 0)
        img = Image.new('RGB', (w, h), background_color)
        drawer = ImageDraw.Draw(img)
        
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if cell:
                    coords = [(x * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size)]
                    drawer.rectangle(coords, fill=fill_color)

        img.save(filename)

    def get_cat(self):
        filename = self.cat_files[self.rand.randint(0, len(self.cat_files) - 1)]
        return Image.open(filename, 'r')

    def get_dog(self):
        filename = self.dog_files[self.rand.randint(0, len(self.dog_files) - 1)]
        return Image.open(filename, 'r')

    def gen_by_matrix(self, matrix, cell_size, filename):
        h = cell_size * len(matrix)
        w = cell_size * len(matrix[0])

        background_color = (255, 255, 255)
        fill_color = (0, 0, 0)
        img = Image.new('RGB', (w, h), background_color)
        drawer = ImageDraw.Draw(img)
        
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if cell:
                    img.paste(self.get_dog(), (x * cell_size, y * cell_size))
                else:
                    img.paste(self.get_cat(), (x * cell_size, y * cell_size))
        
        img.save(filename)

def get_random_string(rand, l):
    return ''.join([rand.choice(string.ascii_uppercase) for _ in range(l)])

def main():

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)

    print("Going to read flags from {}".format(FLAGS_FILE))
    with open('flags.txt') as f:
        secrets = json.load(f)

    print("Going to generate {} files and save them to {} using random seed {}".format(len(secrets), OUTPUT_DIR, RAND_SEED))
    rand = random.Random(RAND_SEED)
    for i, secret in enumerate(secrets):
        flag = secret['flag']
        assert len(flag) <= 21
        output_name = secret['filename']

        matrix_generator = TextMatrixGenerator()
        matrix = matrix_generator.generate_matrix_with_text(flag, 300, 30)

        cat_and_dog_generator = CatAndDogImageGenerator(rand)
        # cat_and_dog_generator.gen_mask_by_matrix(matrix, 50, "output/generated_mask.png") # for debug
        cat_and_dog_generator.gen_by_matrix(matrix, 50, os.path.join(OUTPUT_DIR, output_name))
        print('{}/{} done'.format(i + 1, len(secrets)))
    print('Generation done'.format(i, len(secrets)))

main()
