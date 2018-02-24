#!/usr/bin/python3

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def crop(img):
    w, h = img.size
    sz = min(w, h)
    xCropL, xCropR = (w - sz) // 2, w - (w - sz + 1) // 2
    yCropU, yCropD = (h - sz) // 2, h - (h - sz + 1) // 2
    area = (xCropL, yCropU, xCropR, yCropD)
    return img.crop(area)

def scale(img):
    return img.resize((50, 50), Image.ANTIALIAS)

def process_img(action, input_img, output_img, show=False, save=True):
    img = Image.open(input_img)
    if action == 'crop':
        result = crop(img)
    elif action == 'scale':
        result = scale(img)
    elif action == 'both':
        result = scale(crop(img))
    else:
        raise Exception('Unknown action: "{}"'.format(action))
    if show:
        result.show()
    if save:
        result.save(output_img)

def process_dir(action, input_dir, output_dir, show=False, save=True):
    images = os.listdir(input_dir)
    for i, f in enumerate(images):
        process_img(action, os.path.join(input_dir, f), os.path.join(output_dir, f), show, save)
        if i % 10 == 0:
            print('{}/{}'.format(i, len(images)))

def main():
    if len(sys.argv) < 4:
        print('Usage: {} (file|dir) (crop|scale|both) img_to_crop [save_to]'.format(sys.argv[0]))
        return
    if sys.argv[1] == 'dir':
        if len(sys.argv) == 4:
            process_dir(sys.argv[2], sys.argv[3], None, save=False)
        else:
            process_dir(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        if len(sys.argv) == 4:
            process_img(sys.argv[2], sys.argv[3], None, save=False)
        else:
            process_img(sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
    main()
