import requests
from gmpy2 import next_prime
from json import dumps, loads

COOKIE = {"user":"2|1:0|10:1519559086|4:user|8:YWRtaW4=|f20c4253fc155086a701599057536046ac7e0bab7aedb59e01ec788f00c95ea6"}

if __name__ == "__main__":
    res = 0
    balance = 0
    while balance < 10001:
        r = requests.post("https://browser-mining.contest.qctf.ru/task",data=dumps({"result":res}), cookies=COOKIE)
        data = loads(r.text)
        balance = data['balance']
        print(balance)
        res = int(next_prime(data['task']))