import os
import random

class CipherProvider:
    @staticmethod
    def get_cipher(global_seed, key_len):
        rand = random.Random(global_seed)
        key = [rand.randint(0, 255) for _ in range(key_len)]
        seed = rand.randint(0, 10000)
        return Cipher(key, seed)

class Cipher:
    def __init__(self, key, seed):
        self.key = key
        self.seed = seed

    def encrypt(self, data):
        if len(data) > len(self.key):
            raise Exception("Can encrypt only blocks which are no longer than key length")
        data = [x ^ y for (x, y) in zip(data, self.key)]
        rand = random.Random(self.seed)
        rand.shuffle(data)
        data = [x ^ y for (x, y) in zip(data, self.key)]
        return bytes(data)

    def decrypt(self, data):
        if len(data) > len(self.key):
            raise Exception("Can decrypt only blocks which are no longer than key length")
        data = [x ^ y for (x, y) in zip(data, self.key)]
        perm = list(range(len(data)))
        rand = random.Random(self.seed)
        rand.shuffle(perm)
        unshuffled = [0] * len(data)
        for pos, value in enumerate(perm):
            unshuffled[value] = data[pos]
        data = [x ^ y for (x, y) in zip(unshuffled, self.key)]
        return bytes(data)
