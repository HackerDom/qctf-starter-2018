from PIL import ImageDraw, Image, ImageFont
from lib import *
from sys import argv

if len(argv) != 4:
    print('usage: ./task_generator.py <flag> <image_name> <encoded_name>')
    exit()
flag, image_name, encoded_name = argv[1:]
im = Image.new("RGBA", (500, 500), (255,255,255,255))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('Minecrafter_3.ttf', 60)
for y in range(5):
    draw.text((127,y*80+50),flag[y*5:(y+1)*5],(0,0,0), font=font)

im = prepare_image(im)
with open(encoded_name, 'w') as f: f.write(''.join(map(reverse_second_part, map(cipher_block, read_as_rgb_2x2_blocks(im)))))