import requests
import numpy as np

def main():
    results=[]
    for i in range(100):
        r=requests.get('http://make-some-noise.contest.qctf.ru/<team_id>')
        results.append([ord(x) for x in r.text])
    flag=[]
    for i in range(len(results[0])):
        flag.append(chr(int(round(np.mean(list(map(lambda arr:arr[i], results)))))))
    print(''.join(flag))


if __name__ == '__main__':
    main()