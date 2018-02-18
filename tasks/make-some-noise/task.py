#!/usr/bin/env python3

from random import choice, randint
from math import sqrt
from sys import argv
from socket import socket, SOL_SOCKET, SO_REUSEADDR


def get_noised_flag(flag, noise):
    return [add_noise(x, noise) for x in map(ord,flag)]

def add_noise(x, noise):
    return x + choice(noise)

if __name__ == "__main__":
    if len(argv) != 3:
        print("./task.py <flag> <port>")
        exit()

    FLAG, port = argv[1], int(argv[2])
    n = 40
    noise = list(range(-n, n+1))
    
    with socket() as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            noised_flag = get_noised_flag(FLAG, noise)
            conn.send("{}\r\n".format(str(noised_flag)).encode())
            conn.close()