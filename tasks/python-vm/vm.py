##!/usr/bin/python3

import struct
import sys
import inspect
import hashlib

from inspect import signature, BoundArguments

from abc import abstractmethod, ABC
from functools import wraps


BYTE_VALUE  = 1
WORD_VALUE  = 2
DWORD_VALUE = 4

BYTE_FMT  = 'b'
WORD_FMT  = 'h'
DWORD_FMT = 'i'

REGISTER = 0x50
CONSTANT = 0x60

NULLVALUE = 0

SIZES = [BYTE_VALUE, WORD_VALUE, DWORD_VALUE]

SIZE2FMT = {
    BYTE_VALUE:  BYTE_FMT,
    WORD_VALUE:  WORD_FMT,
    DWORD_VALUE: DWORD_FMT,
}

MEMORY_SIZE = 0x6000

TEXT_SECTION_RANGE  = (0x0000, 0x0fff)
HEAP_SECTION_RANGE  = (0x1fff, 0x2fff)
STACK_SECTION_RANGE = (0x3fff, 0x5fff)


def load_memory():
    program_memory = ''
    with open('memory', 'rb') as mem:
        program_memory = bytearray(mem.read())
    return program_memory, bytearray([0] * 0xfff)


def get_params_count(func):
    return len(signature(func).parameters)


def type_correct(instruction):
    @wraps(instruction)
    def validation(*args):
        sign = signature(instruction)
        bound_args = sign.bind(*args)
        for arg_name, arg_value in bound_args.arguments.items():
            annotation = sign.parameters[arg_name].annotation
            if annotation != inspect._empty and (not isinstance(arg_value, annotation)):
                raise InvalidArgumentType("Incorrect argument type!")
        instruction(*args)
    return validation


def find_size(num):
    size_info = -1
    for fmt, size in [('b', BYTE_VALUE), ('h', WORD_VALUE), ('i', DWORD_VALUE)][::-1]:
        try:
            struct.pack(fmt, num)
            size_info = size
        except Exception:
            return size_info
    return size_info


class PermissionException(Exception):
    pass


class InvalidOperandSize(Exception):
    pass


class InvalidValueSize(Exception):
    pass


class InstructionError(Exception):
    pass


class InvalidArgumentType(ValueError):
    pass


class ReadMemoryException(Exception):
    pass


class WriteMemoryException(Exception):
    pass


class StackRangeCorrupted(Exception):
    pass


class Operand(ABC):
    def __init__(self, val, size=BYTE_VALUE):
        if size not in SIZES:
            raise InvalidOperandSize("You have an invalid operand size!")

        super().__init__()

        self.size  = size
        self.__value = val

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, num):
        self.__value = num


class Constant(Operand):
    def __init__(self, val=0, size=DWORD_VALUE):
        super().__init__(val, size)


class BaseRegister(Operand):
    def __init__(self, memory_handler, mem_offset, val=0, size=DWORD_VALUE):
        super().__init__(val, size)

        self.memory_handler = memory_handler
        self.offset = mem_offset
        self.value  = val

    @property
    def value(self):
        return self.memory_handler.read(self.offset, self.size)

    @value.setter
    def value(self, operand):
        def set_value(value, size):
            if size > self.size:
                raise InvalidOperandSize("Invalid operand size!")
            self.memory_handler.write(self.offset, self.size, value)

        if isinstance(operand, Operand):
            set_value(operand.value, operand.size)
        elif isinstance(operand, int):
            set_value(operand, find_size(operand))
        else:
            raise InstructionError("Incorrect instruction")


class ByteRegister(BaseRegister):
    def __init__(self, memory_handler, mem_offset, val=0):
        super().__init__(memory_handler, mem_offset, val, BYTE_VALUE)


class WordRegister(BaseRegister):
    def __init__(self, memory_handler, mem_offset, val=0):
        super().__init__(memory_handler, mem_offset, val, WORD_VALUE)


class DwordRegister(BaseRegister):
    def __init__(self, memory_handler, mem_offset, val=0):
        super().__init__(memory_handler, mem_offset, val, DWORD_VALUE)


class Register:
    def __init__(self, memory_handler, mem_offset, value=0):
        self.offset = mem_offset
        self.memory_handler = memory_handler

        self.reg_byte  = ByteRegister(memory_handler, mem_offset)
        self.reg_word  = WordRegister(memory_handler, mem_offset)
        self.reg_dword = DwordRegister(memory_handler, mem_offset)

        self.reg_dword.value = value

        self.matching = {
            BYTE_VALUE:  self.reg_byte,
            WORD_VALUE:  self.reg_word,
            DWORD_VALUE: self.reg_dword
        }

    def get(self, size):
        return self.matching[size]


class MemoryHandler:
    def __init__(self, memory):
        self.memory = memory

    def read_string(self, address):
        buf = bytearray(b'')
        while self.read_byte(address) != NULLVALUE:
            buf.append(self.read_byte(address))
            address += 1
        return buf

    def write_string(self, address, string):
        string += b'\x00'
        for index in range(len(string)):
            self.write_byte(address+index, string[index])

    def read(self, address, size):
        try:
            return struct.unpack(SIZE2FMT[size], self.memory[address:address+size])[0]
        except Exception:
            raise ReadMemoryException('Error occurred while trying to read a memory')

    def write(self, address, size, value):
        try:
            write_value = struct.pack(SIZE2FMT[size], value)
            self.memory[address:address+len(write_value)] = write_value
        except Exception:
            raise WriteMemoryException('Error occurred while trying to write to a memory')

    def read_byte(self, address):
        return self.read(address, BYTE_VALUE)

    def read_word(self, address):
        return self.read(address, WORD_VALUE)

    def read_dword(self, address):
        return self.read(address, DWORD_VALUE)

    def write_byte(self, address, value):
        self.write(address, BYTE_VALUE, value)

    def write_word(self, address, value):
        self.write(address, WORD_VALUE, value)

    def write_dword(self, address, value):
        self.write(address, DWORD_VALUE, value)


class MemoryStream:
    def __init__(self, memory_handler: MemoryHandler, pointer, pointer_get_value_func, pointer_add_func):
        self.pointer        = pointer
        self.add_func       = pointer_add_func
        self.get_value_func = pointer_get_value_func

        self.memory_handler = memory_handler

        self.size_to_read = {
            BYTE_VALUE:  self.read_byte,
            WORD_VALUE:  self.read_word,
            DWORD_VALUE: self.read_dword
        }

    def read(self, size):
        return self.size_to_read[size]()

    def read_byte(self):
        byte = self.memory_handler.read_byte(self.get_value_func(self.pointer))
        self.add_func(self.pointer, BYTE_VALUE)
        return byte

    def read_word(self):
        word = self.memory_handler.read_word(self.get_value_func(self.pointer))
        self.add_func(self.pointer, WORD_VALUE)
        return word

    def read_dword(self):
        dword = self.memory_handler.read_dword(self.get_value_func(self.pointer))
        self.add_func(self.pointer, DWORD_VALUE)
        return dword


class Assembly:
    def __init__(self, mem_handler: MemoryHandler, IP: DwordRegister, SP: DwordRegister, regs: list):
        self.IP   = IP
        self.SP   = SP
        self.regs = regs
        self.FLAGS = [0, 0, 0] # Is Less [IL], Is Greater [IG], Is Equal [IE]

        self.mem_handler = mem_handler

    def update_flags(self, val):
        if val == 0:
            self.FLAGS[2] = 1
        elif val < 0:
            self.FLAGS[0] = 1
        else:
            self.FLAGS[1] = 1

    def clear_flags(self):
        self.FLAGS = [0, 0, 0]

    @type_correct
    def mov(self, f: BaseRegister, s: Operand):
        f.value = s

    @type_correct
    def load(self, f: BaseRegister, s: Operand):
        mem_ptr  = s.value
        reg_size = f.size
        memory_value = self.mem_handler.read(mem_ptr, reg_size)
        f.value = Constant(memory_value, reg_size)

    @type_correct
    def store(self, f: BaseRegister, s: Operand):
        mem_ptr  = s.value
        reg_size = f.size
        if (TEXT_SECTION_RANGE[0] <= mem_ptr <= TEXT_SECTION_RANGE[1]):
            raise PermissionException("You don't have a permission to write into .text section!")
        self.mem_handler.write(mem_ptr, reg_size, f.value)

    @type_correct
    def add(self, f: BaseRegister, s: Operand):
        f.value += s.value

    @type_correct
    def sub(self, f: BaseRegister, s: Operand):
        f.value = f.value - s.value

    @type_correct
    def xor(self, f: BaseRegister, s: Operand):
        f.value ^= s.value

    @type_correct
    def inc(self, f: BaseRegister):
        f.value += 1

    @type_correct
    def dec(self, f: BaseRegister):
        f.value -= 1

    @type_correct
    def div(self, f: BaseRegister, s: Operand):
        f.value //= s.value

    @type_correct
    def mod(self, f: BaseRegister, s: Operand):
        f.value %= s.value

    @type_correct
    def cmp(self, f: BaseRegister, s: Operand):
        self.clear_flags()
        self.update_flags(f.value - s.value)

    @type_correct
    def jmp(self, f: Constant):
        self.IP.value = f

    @type_correct
    def je(self, f: Constant):
        if self.FLAGS[2]:
            self.jmp(f)

    @type_correct
    def jne(self, f: Constant):
        if not self.FLAGS[2]:
            self.jmp(f)

    @type_correct
    def jg(self, f: Constant):
        if self.FLAGS[1]:
            self.jmp(f)

    @type_correct
    def jl(self, f: Constant):
        if self.FLAGS[0]:
            self.jmp(f)

    def __hash(self, hash_handler, value_address, address):
        buf = self.mem_handler.read_string(value_address)
        hash_handler.update(buf)
        hex_hash = hash_handler.hexdigest()
        self.mem_handler.write_string(address, hex_hash.encode())

    @type_correct
    def hash_md5(self, f: BaseRegister, s: Constant):
        self.__hash(hashlib.md5(), f.value, s.value)

    @type_correct
    def hash_sha1(self, f: BaseRegister, s: Constant):
        self.__hash(hashlib.sha1(), f.value, s.value)

    @type_correct
    def puts(self, f: BaseRegister):
        buf = self.mem_handler.read_string(f.value)
        print(buf.decode())

    @type_correct
    def gets(self, f: BaseRegister):
        buf = bytearray(input().encode())
        self.mem_handler.write_string(f.value, buf)

    @type_correct
    def strcmp(self, f: BaseRegister, s: BaseRegister, t: BaseRegister):
        buf1 = self.mem_handler.read_string(f.value)
        buf2 = self.mem_handler.read_string(s.value)
        t.value = int(buf1 == buf2)

    @type_correct
    def push(self, reg: BaseRegister):
        if self.SP.value <= STACK_SECTION_RANGE[0]:
            raise StackRangeCorrupted("Pushing is happening when the stack is full.")
        self.SP.value = self.SP.value - DWORD_VALUE
        self.store(reg, self.SP)

    @type_correct
    def pop(self, reg: BaseRegister):
        if self.SP.value >= STACK_SECTION_RANGE[1]:
            raise StackRangeCorrupted("Pop is happening when the stack is empty!")
        self.load(reg, self.SP)
        self.SP.value = self.SP.value + DWORD_VALUE

    def exit(self):
        sys.exit()


class VirtualMachine:
    def __init__(self, program_memory, register_memory):
        def add_value(operand, value):
            operand.value = operand.value + value

        self.memory_handler = MemoryHandler(program_memory)
        self.reg_mem_handler = MemoryHandler(register_memory)

        self.init_registers(self.reg_mem_handler)
        self.asm = Assembly(self.memory_handler, self.IP, self.SP, self.regs)

        self.init_matches()

        self.IP_stream = MemoryStream(self.memory_handler, self.IP, lambda operand: operand.value, add_value)

    def init_matches(self):
        self.oprdcode = {
            REGISTER: Register,
            CONSTANT: Constant
        }

        self.opcode = {
            0x10: self.asm.mov,
            0x11: self.asm.load,
            0x12: self.asm.store,
            0x13: self.asm.add,
            0x14: self.asm.sub,
            0x15: self.asm.xor,
            0x16: self.asm.inc,
            0x17: self.asm.dec,
            0x18: self.asm.cmp,
            0x19: self.asm.jmp,
            0x1a: self.asm.je,
            0x1b: self.asm.jg,
            0x1c: self.asm.jl,
            0x26: self.asm.jne,
            0x1e: self.asm.puts,
            0x1f: self.asm.gets,
            0x20: self.asm.push,
            0x21: self.asm.pop,
            0x22: self.asm.div,
            0x23: self.asm.mod,
            0x24: self.asm.hash_md5,
            0x25: self.asm.hash_sha1,
            0x27: self.asm.strcmp,
            0x00: self.asm.exit
        }

    def init_registers(self, mem_handler):
        self.IP = DwordRegister(mem_handler, 0)
        self.SP = DwordRegister(mem_handler, 8, STACK_SECTION_RANGE[1])

        self.regs = []
        for i in range(16):
            offset = 8 * (i+3)
            self.regs.append(Register(mem_handler, offset))

    def get_operand(self):
        operand_type = self.IP_stream.read_byte()
        if operand_type == REGISTER:
            reg_index   = self.IP_stream.read_byte()
            size        = self.IP_stream.read_byte()
            return self.regs[reg_index].get(size)
        elif operand_type == CONSTANT:
            val_size = self.IP_stream.read_byte()
            val      = self.IP_stream.read(val_size)
            return Constant(val, val_size)
        else:
            raise InstructionError("Error occurred while executing an instruction")

    def exec(self):
        operands = []
        instruction = self.opcode[self.IP_stream.read_byte()]
        for _ in range(get_params_count(instruction)):
            operands.append(self.get_operand())
        instruction(*operands)

    def run(self):
        while True:
            self.exec()


def main():
    program_memory, register_memory = load_memory()

    vm = VirtualMachine(program_memory, register_memory)
    vm.run()


if __name__ == '__main__':
    main()