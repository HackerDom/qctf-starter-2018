import re
import struct
import binascii

from vm import VirtualMachine
from vm import REGISTER, CONSTANT


# WARNING!
# Please, forget about code readability and other stupid OOP things
# This is hardcore unreadable code. Don't die while reading it
# (c) merrychap


WORD = 'W'
BYTE = 'B'

JUMPS  = ['jmp', 'je', 'jl', 'jg', 'jne']


class InvalidOperation(Exception):
    pass


class InvalidOperand(Exception):
    pass


class Interpreter:
    def __init__(self, opcodes):
        self.opcode = opcodes

        self.reg     = re.compile(r'^((R\d)|(R\d(W|B)))$')
        self.num     = re.compile(r'^(\d+)$')
        self.r_three = re.compile(r'^(\w+)[ ]+([\w\d]*?),[ ]+([\w\d]*),[ ]+([\w\d]*)[\w\W]*$')
        self.r_two   = re.compile(r'^(\w+)[ ]+([\w\d]*?),[ ]+([\w\d]*)[\w\W]*$')
        self.r_one   = re.compile(r'^(\w+)[ ]+([\w\d]*)[\w\W]*$')
        self.label   = re.compile(r'^([\w_\d]+):$')
        self.r_none  = re.compile(r'^([\w]+)$')

        self.string = re.compile(r'^([\w\W]+)$')

        self.line_regex = [
            (self.label,   self.handle_label),
            (self.r_three, self.handle_r_three),
            (self.r_two,   self.handle_r_two),
            (self.r_one,   self.handle_r_one),
            (self.r_none,  self.handle_r_none)
        ]

        self.labels_matching = {}

    def handle_r_three(self, match, bc_len=-1):
        buf = bytearray(b'')
        inst, op1, op2, op3 = match.groups()
        return bytearray([self.opcode[inst]]) + self.parse_op(op1) + self.parse_op(op2) + self.parse_op(op3)

    def handle_r_two(self, match, bc_len=-1):
        buf = bytearray(b'')
        inst, op1, op2 = match.groups()
        return bytearray([self.opcode[inst]]) + self.parse_op(op1) + self.parse_op(op2)

    def handle_r_one(self, match, bc_len=-1):
        inst, op = match.groups()
        return bytearray([self.opcode[inst]]) + self.parse_op(op)

    def handle_r_none(self, match, bc_len=-1):
        inst = match.groups()
        return bytearray([self.opcode[inst[0]]])

    def handle_label(self, match, bc_len=-1):
        self.labels_matching[match.groups()[0]] = bc_len
        return bytearray(b'')

    def to_bytes(self, num, size='B'):
        return struct.pack(size, num).decode()

    def find_size(self, num):
        rsz = -1
        for fmt, sz in [('b', 1), ('h', 2), ('i', 4)][::-1]:
            try:
                struct.pack(fmt, num)
                rsz = (fmt, sz)
            except Exception:
                return rsz
        return rsz

    def parse_op(self, op):
        def parse_reg(reg):
            if reg[-1] == BYTE:
                return bytearray([REGISTER, int(reg[1]), 0x01])
            elif reg[-1] == WORD:
                return bytearray([REGISTER, int(reg[1]), 0x02])
            else:
                return bytearray([REGISTER, int(reg[1]), 0x04])

        reg  = self.reg.match(op)
        num  = self.num.match(op)
        _str = self.string.match(op)

        if reg:
            r = reg.groups()[0]
            return parse_reg(r)
        elif num:
            n = int(num.groups()[0])
            return bytearray([CONSTANT]) + struct.pack('B', 4) + struct.pack('i', n)
        elif _str:
            label = _str.groups()[0]
            return bytearray(b'\x00\x00\x00\x00\x00\x00')
        else:
            raise InvalidOperand("Your code have an invalid operand")

    def __trans(self, code: list):
        bytecode = bytearray(b'')
        for line in code:
            if line == '':
                continue
            # print(len(bytecode), line)
            is_matched = False
            buf = bytearray(b'')
            for regex, handle in self.line_regex:
                match = regex.match(line)
                if match:
                    is_matched = True
                    buf = handle(match, len(bytecode))
                    break
            if not is_matched:
                raise InvalidOperation("You have an invalid operation in your code")
            bytecode += buf
        return bytecode

    def jmp_correction(self, code: list):
        newcode = []

        for line in code:
            if line == '':
                continue
            sline = list(filter(None, line.split(' ')))
            if sline[0] in JUMPS:
                newcode.append('{} {}'.format(sline[0], str(self.labels_matching[sline[1]])))
            else:
                newcode.append(line)
        return newcode

    def translate(self, code: list):
        _     = self.__trans(code)
        ncode = self.jmp_correction(code)
        return self.__trans(ncode)


def gen_bytecode():
    '''
    Positions of different strings:

    heap_start:        8191
    first_bytes:       10239
    middle_bytes_hash: 10339
    last_bytes_hash:   10439
    enflag:            10539
    error_msg:         10639
    hardcoded:         10739
    enter_string:      10839
    memory_end:        24575
    '''

    code = ''
    with open('asm_code', 'r') as asmfile:
        code = asmfile.read()

    vm = VirtualMachine(bytearray(b''), bytearray([0] * 0xfff))
    inter = Interpreter({v.__name__: k for k, v in vm.opcode.items()})
    bytecode = inter.translate(code.split('\n'))

    return bytecode


def main():
    bytecode = gen_bytecode()
    for x in bytecode:
        print("\\x{:02x}".format(ord(x)), end="")


if __name__ ==  '__main__':
    main()