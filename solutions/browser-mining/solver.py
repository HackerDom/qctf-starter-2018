import requests
from gmpy2 import next_prime
from json import dumps, loads

COOKIE = {"user":"2|1:0|10:1519228376|4:user|8:bWlzaGE=|e1bff59ad24b2ebdd65feab17e88155a1b7a8bbd441ad162738d094c755e14e0"}

if __name__ == "__main__":
    res = 0
    balance = 0
    while balance < 10001:
        r = requests.post("http://localhost:8888/task",data=dumps({"result":res}), cookies=COOKIE)
        data = loads(r.text)
        balance = data['balance']
        print(balance)
        res = int(next_prime(data['task']))