import re
import struct
import binascii

from vm import VirtualMachine
from vm import BYTEREG, WORDREG, DWORDREG, MEMORYPTR, INTEGER


WORD = 'W'
BYTE = 'B'

JUMPS  = ['jmp', 'je', 'jl', 'jg']


class InvalidOperation(Exception):
    pass


class InvalidOperand(Exception):
    pass


class Interpreter:
    def __init__(self, opcodes):
        self.opcode = opcodes

        self.reg    = re.compile(r'^((R\d)|(R\d(W|B)))$')
        self.ptr    = re.compile(r'^\[((R\d)|(R\d(W|B)))\]$')
        self.num    = re.compile(r'^(\d+)$')
        self.r_two  = re.compile(r'^(\w+)[ ]+(.*?),[ ]+(.*?)$')
        self.r_one  = re.compile(r'^(\w+)[ ]+(.*?)$')

    def to_bytes(self, num, size='B'):
        return struct.pack(size, num).decode()

    def find_size(self, num):
        rsz = -1
        for fmt, sz in [('B', 1), ('H', 2), ('I', 4)][::-1]:
            try:
                struct.pack(fmt, num)
                rsz = (fmt, sz)
            except Exception:
                return rsz
        return rsz

    def parse_op(self, op):
        def parse_reg(reg):
            if reg[-1] == BYTE:
                return BYTEREG + self.to_bytes(int(reg[1]))
            elif reg[-1] == WORD:
                return WORDREG + self.to_bytes(int(reg[1]))
            else:
                return DWORDREG + self.to_bytes(int(reg[1]))

        reg = self.reg.match(op)
        ptr = self.ptr.match(op)
        num = self.num.match(op)
        if reg:
            r = reg.groups()[0]
            return parse_reg(r) + '\x00'
        elif ptr:
            p = ptr.groups()[0]
            return parse_reg(p) + '\x01'
        elif num:
            n = int(num.groups()[0])
            # fmt, rsz = self.find_size(n)
            fmt, rsz = 'I', 4
            return INTEGER + (struct.pack('B', rsz) + struct.pack(fmt, n)).decode('unicode_escape')
        else:
            raise InvalidOperand("Your code have an invalid operand")

    def __trans(self, code: list):
        bpref    = []
        bytecode = ''
        for line in code:
            if line == '':
                continue
            buf     = ''
            match_2 = self.r_two.match(line)
            match_1 = self.r_one.match(line)
            if match_2:
                inst, op1, op2 = match_2.groups()
                buf += self.opcode[inst]
                buf += self.parse_op(op1)
                buf += self.parse_op(op2)
            elif match_1:
                inst, op = match_1.groups()
                buf += self.opcode[inst]
                buf += self.parse_op(op)
            else:
                raise InvalidOperation("You have an invalid operation in your code")
            bpref.append(len(bytecode))
            bytecode += buf
        return bytecode, bpref

    def jmp_correction(self, code: list, bpref: list):
        newcode = []
        for line in code:
            if line == '':
                continue
            sline = list(filter(None, line.split(' ')))
            if sline[0] in JUMPS:
                newcode.append('{} {}'.format(sline[0], str(bpref[int(sline[1])-1])))
            else:
                newcode.append(line)
        return newcode

    def translate(self, code: list):
        _, bpref = self.__trans(code)
        ncode    = self.jmp_correction(code, bpref)
        return self.__trans(ncode)[0]


def main():
    vm       = VirtualMachine()
    inter    = Interpreter({v.__name__: k for k, v in vm.opcode.items()})
    bytecode = inter.translate(
'''
load R1, 0
load R0, 0
load R2, 3
cmp  R0, R2
je   9
add R1, 5
inc R0
jmp  4
load R3, R1
'''.split('\n'))
    for x in bytecode:
        print("\\x{:02x}".format(ord(x)), end="")


if __name__ ==  '__main__':
    main()