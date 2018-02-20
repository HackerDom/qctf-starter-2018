from lib import *
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 task.py <image_name> <encrypted_name>")
        exit()
    with open(sys.argv[2], 'w') as f: f.write(''.join(map(reverse_second_part, map(cipher_block, read_as_rgb_2x2_blocks(sys.argv[1])))))