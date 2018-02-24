from PIL import Image
from random import randint
from numpy import array


def make_color(): return (randint(0,255), randint(0,255), randint(0,255))

def main():
    with open('task.txt', 'r') as f: data = f.read()
    data = [data[i*10:(i+1)*10] for i in range(len(data)//10)]
    colors = {x:make_color() for x in set(data)}
    colored_data = [colors[x] for x in data]
    colored_data = list(zip(*(colored_data[250*i:250*(i+1)] for i in range(250))))
    colored_data = array(colored_data).astype('uint8')
    Image.fromarray(colored_data, 'RGB').show()

if __name__ == "__main__":
    main()