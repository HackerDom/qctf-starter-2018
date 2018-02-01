from lib import *

image = 'task.png'

if __name__ == "__main__": 
    with open('task.txt', 'w') as f: f.write(''.join(map(reverse_second_part, map(cipher_block, read_as_rgb_2x2_blocks(image)))))