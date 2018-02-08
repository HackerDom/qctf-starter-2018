#!/usr/bin/env python3

from socket import socket
from ast import literal_eval


def get_flag():
    with socket() as s:
        s.connect(('', 8888))
        shift, array = s.recv(1024).decode().split('\r\n')[:-1]
        shift = int(shift.split()[1])
        array = literal_eval(array.split(' ',1)[1])
        return array[-shift:] + array[:-shift]

if __name__ == "__main__":
    array = []
    for i in range(100000):
        res = get_flag()
        array.append(res)
        print(i, ''.join(map(chr, (round(sum(x) / len(x)) for x in zip(*array)))))