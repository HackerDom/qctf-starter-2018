#!/usr/bin/env python3

from ast import literal_eval
import requests

TEAM_ID = "SOmxD7RqEXLQDFd2CRtB"

def get_flag():
    r = requests.get("http://127.0.0.1:8889/{}".format(TEAM_ID))
    return literal_eval(r.text)

if __name__ == "__main__":
    array = []
    for i in range(100000):
        res = get_flag()
        array.append(res)
        print(i, ''.join(map(chr, (round(sum(x) / len(x)) for x in zip(*array)))))