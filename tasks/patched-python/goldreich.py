import itertools
import random


N = 128
D = 10
SEED = 'substitutethis'


def generate_subsets(n, d):
    S = []
    indices = range(n)
    for _ in range(n):
        S.append(sorted(random.sample(indices, d)))
    return S


def construct_predicate(true_arguments):
    def predicate(bit_string):
        return '1' if bit_string in true_arguments else '0'
    return predicate


def generate_predicate(d):
    true_arguments = set()
    for bit_string in itertools.product('01', repeat=d):
        if random.random() < 0.5:
            true_arguments.add(''.join(bit_string))
    return construct_predicate(true_arguments)


def construct_owf(subsets, predicate):
    def owf(bit_string):
        return ''.join(
            predicate(''.join(
                bit_string[index]
                for index in subset))
            for subset in subsets)
    return owf


def generate_owf(n, d):
    return construct_owf(generate_subsets(n, d), generate_predicate(d))


def generate_input(n):
    return ''.join(random.choice('01') for _ in range(n))


def format_output(bit_string):
    return hex(int(bit_string, 2))[2:]


def main(seed):
    random.seed(seed)
    return 'QCTF{{{}}}'.format(format_output(generate_owf(N, D)(generate_input(N))))


if __name__ == '__main__':
    print(main(SEED))
