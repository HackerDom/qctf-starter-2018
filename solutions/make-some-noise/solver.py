import requests
import numpy as np

def main():
    results=[]
    for i in range(100):
        r=requests.get('https://make-some-noise.contest.qctf.ru/2TjUAurc7P60IBLM2qCe')
        results.append([ord(x) for x in r.text])
        flag = (chr(int(round(np.mean(list(map(lambda arr:arr[i], results)))))) for i in range(len(results[0])))
        print(''.join(flag))


if __name__ == '__main__':
    main()