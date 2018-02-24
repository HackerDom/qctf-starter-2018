#!/usr/bin/python3

import struct
import sys
import inspect
import hashlib

from inspect import signature

from abc import ABC
from functools import wraps


BYTE_SIZE  = 1
WORD_SIZE  = 2
DWORD_SIZE = 4

REGISTER_OPERAND = 0x50
CONSTANT_OPERAND = 0x60

NULLBYTE = 0

SUPPORTED_SIZES = [BYTE_SIZE, WORD_SIZE, DWORD_SIZE]

MEMORY_SIZE = 0x6000

TEXT_SECTION_RANGE  = (0x0000, 0x0fff)
HEAP_SECTION_RANGE  = (0x1fff, 0x2fff)
STACK_SECTION_RANGE = (0x3fff, 0x5fff)


def load_memory():
    with open('memory', 'rb') as mem:
        program_memory = bytearray(mem.read())
    return program_memory


def get_params_count(func):
    return len(signature(func).parameters)


def type_checking(instruction):
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
    for fmt, size in [('i', DWORD_SIZE), ('h', WORD_SIZE), ('b', BYTE_SIZE)]:
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


class InvalidStackRange(Exception):
    pass


class ExitInterruption(Exception):
    pass


class Operand(ABC):
    def __init__(self, size=BYTE_SIZE):
        if size not in SUPPORTED_SIZES:
            raise InvalidOperandSize("You have an invalid operand size!")

        super().__init__()

        self.size  = size

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, num):
        self._value = num


class Constant(Operand):
    def __init__(self, val=0, size=DWORD_SIZE):
        super().__init__(size)

        self._value = val


class BaseRegister(Operand):
    def __init__(self, bytes_handler, offset, val=0, size=DWORD_SIZE):
        super().__init__(size)

        self.bytes_handler = bytes_handler
        self.offset = offset
        self.value  = val

    @property
    def value(self):
        return self.bytes_handler.read(self.offset, self.size)

    @value.setter
    def value(self, operand):
        if isinstance(operand, Operand):
            self.set_value(operand.value, operand.size)
        elif isinstance(operand, int):
            self.set_value(operand, find_size(operand))
        else:
            raise InstructionError("Cannot assign a value to the register's value")

    def set_value(self, value, size):
        if size > self.size:
            raise InvalidOperandSize("Size of a source operand greater than the size of a destination operand!")
        self.bytes_handler.write(self.offset, self.size, value)


class ByteRegister(BaseRegister):
    def __init__(self, bytes_handler, offset, val=0):
        super().__init__(bytes_handler, offset, val, BYTE_SIZE)


class WordRegister(BaseRegister):
    def __init__(self, bytes_handler, offset, val=0):
        super().__init__(bytes_handler, offset, val, WORD_SIZE)


class DwordRegister(BaseRegister):
    def __init__(self, bytes_handler, offset, val=0):
        super().__init__(bytes_handler, offset, val, DWORD_SIZE)


class Register:
    def __init__(self, memory_handler, mem_offset, value=0):
        self.offset = mem_offset
        self.memory_handler = memory_handler

        self.reg_byte  = ByteRegister(memory_handler, mem_offset)
        self.reg_word  = WordRegister(memory_handler, mem_offset)
        self.reg_dword = DwordRegister(memory_handler, mem_offset)

        self.reg_dword.value = value

        self.matching = {
            BYTE_SIZE:  self.reg_byte,
            WORD_SIZE:  self.reg_word,
            DWORD_SIZE: self.reg_dword
        }

    def get(self, size):
        return self.matching[size]


class BytesHandler:
    def __init__(self, bytes):
        self.bytes   = bytes
        self.size2fmt = {
            BYTE_SIZE:  'b',
            WORD_SIZE:  'h',
            DWORD_SIZE: 'i',
        }

    def read_string(self, address):
        buf = bytearray(b'')
        while self.read_byte(address) != NULLBYTE:
            buf.append(self.read_byte(address))
            address += 1
        return buf

    def write_string(self, address, string):
        string += b'\x00'
        for index in range(len(string)):
            self.write_byte(address+index, string[index])

    def read(self, address, size):
        try:
            return struct.unpack(self.size2fmt[size], self.bytes[address:address + size])[0]
        except Exception:
            raise ReadMemoryException('Error occurred while trying to read a memory')

    def write(self, address, size, value):
        try:
            write_value = struct.pack(self.size2fmt[size], value)
            self.bytes[address:address + len(write_value)] = write_value
        except Exception:
            raise WriteMemoryException('Error occurred while trying to write to a memory')

    def read_byte(self, address):
        return self.read(address, BYTE_SIZE)

    def read_word(self, address):
        return self.read(address, WORD_SIZE)

    def read_dword(self, address):
        return self.read(address, DWORD_SIZE)

    def write_byte(self, address, value):
        self.write(address, BYTE_SIZE, value)

    def write_word(self, address, value):
        self.write(address, WORD_SIZE, value)

    def write_dword(self, address, value):
        self.write(address, DWORD_SIZE, value)


class MemoryStream:
    def __init__(self, memory_handler: BytesHandler, pointer, pointer_get_value_func, pointer_add_func):
        self.pointer        = pointer
        self.add_func       = pointer_add_func
        self.get_value_func = pointer_get_value_func

        self.memory_handler = memory_handler

        self.size_to_read = {
            BYTE_SIZE:  self.read_byte,
            WORD_SIZE:  self.read_word,
            DWORD_SIZE: self.read_dword
        }

    def read(self, size):
        return self.size_to_read[size]()

    def read_byte(self):
        byte = self.memory_handler.read_byte(self.get_value_func(self.pointer))
        self.add_func(self.pointer, BYTE_SIZE)
        return byte

    def read_word(self):
        word = self.memory_handler.read_word(self.get_value_func(self.pointer))
        self.add_func(self.pointer, WORD_SIZE)
        return word

    def read_dword(self):
        dword = self.memory_handler.read_dword(self.get_value_func(self.pointer))
        self.add_func(self.pointer, DWORD_SIZE)
        return dword


class Assembly:
    def __init__(self, mem_handler: BytesHandler, IP: DwordRegister, SP: DwordRegister, regs: list):
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

    @type_checking
    def mov(self, f: BaseRegister, s: Operand):
        f.value = s

    @type_checking
    def load(self, f: BaseRegister, s: Operand):
        mem_ptr  = s.value
        reg_size = f.size
        memory_value = self.mem_handler.read(mem_ptr, reg_size)
        f.value = Constant(memory_value, reg_size)

    @type_checking
    def store(self, f: BaseRegister, s: Operand):
        mem_ptr  = s.value
        reg_size = f.size
        if (TEXT_SECTION_RANGE[0] <= mem_ptr <= TEXT_SECTION_RANGE[1]):
            raise PermissionException("You don't have a permission to write into .text section!")
        self.mem_handler.write(mem_ptr, reg_size, f.value)

    @type_checking
    def add(self, f: BaseRegister, s: Operand):
        f.value += s.value

    @type_checking
    def sub(self, f: BaseRegister, s: Operand):
        f.value = f.value - s.value

    @type_checking
    def xor(self, f: BaseRegister, s: Operand):
        f.value ^= s.value

    @type_checking
    def inc(self, f: BaseRegister):
        f.value += 1

    @type_checking
    def dec(self, f: BaseRegister):
        f.value -= 1

    @type_checking
    def div(self, f: BaseRegister, s: Operand):
        f.value //= s.value

    @type_checking
    def mod(self, f: BaseRegister, s: Operand):
        f.value %= s.value

    @type_checking
    def cmp(self, f: BaseRegister, s: Operand):
        self.clear_flags()
        self.update_flags(f.value - s.value)

    @type_checking
    def jmp(self, f: Constant):
        self.IP.value = f

    @type_checking
    def je(self, f: Constant):
        if self.FLAGS[2]:
            self.jmp(f)

    @type_checking
    def jne(self, f: Constant):
        if not self.FLAGS[2]:
            self.jmp(f)

    @type_checking
    def jg(self, f: Constant):
        if self.FLAGS[1]:
            self.jmp(f)

    @type_checking
    def jl(self, f: Constant):
        if self.FLAGS[0]:
            self.jmp(f)

    def __hash(self, hash_handler, value_address, address):
        buf = self.mem_handler.read_string(value_address)
        hash_handler.update(buf)
        hex_hash = hash_handler.hexdigest()
        self.mem_handler.write_string(address, hex_hash.encode())

    @type_checking
    def hash_md5(self, f: BaseRegister, s: Constant):
        self.__hash(hashlib.md5(), f.value, s.value)

    @type_checking
    def hash_sha1(self, f: BaseRegister, s: Constant):
        self.__hash(hashlib.sha1(), f.value, s.value)

    @type_checking
    def puts(self, f: BaseRegister):
        buf = self.mem_handler.read_string(f.value)
        print(buf.decode())

    @type_checking
    def gets(self, f: BaseRegister):
        buf = bytearray(input().encode())
        self.mem_handler.write_string(f.value, buf)

    @type_checking
    def strcmp(self, f: BaseRegister, s: BaseRegister):
        buf1 = self.mem_handler.read_string(f.value).hex()
        buf2 = self.mem_handler.read_string(s.value).hex()

        self.clear_flags()
        self.update_flags(int(buf1, 16) - int(buf2, 16))

    @type_checking
    def push(self, reg: BaseRegister):
        if self.SP.value <= STACK_SECTION_RANGE[0]:
            raise InvalidStackRange("Pushing is happening when the stack is full.")
        self.SP.value = self.SP.value - DWORD_SIZE
        self.store(reg, self.SP)

    @type_checking
    def pop(self, reg: BaseRegister):
        if self.SP.value >= STACK_SECTION_RANGE[1]:
            raise InvalidStackRange("Pop is happening when the stack is empty!")
        self.load(reg, self.SP)
        self.SP.value = self.SP.value + DWORD_SIZE

    def exit(self):
        raise ExitInterruption()


class VirtualMachine:
    def __init__(self, program_memory):
        def add_value(operand, value):
            operand.value += value

        register_memory = bytearray([0] * 0xfff)

        self.memory_handler = BytesHandler(program_memory)
        self.reg_mem_handler = BytesHandler(register_memory)

        self.init_registers(self.reg_mem_handler)
        self.asm = Assembly(self.memory_handler, self.IP, self.SP, self.regs)

        self.init_matches()

        self.IP_stream = MemoryStream(self.memory_handler, self.IP, lambda operand: operand.value, add_value)

    def init_matches(self):
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
        self.SP = DwordRegister(mem_handler, 4, STACK_SECTION_RANGE[1])

        self.regs = []
        offset = 8
        for i in range(16):
            self.regs.append(Register(mem_handler, offset))
            offset += DWORD_SIZE

    def get_operand(self):
        operand_type = self.IP_stream.read_byte()
        if operand_type == REGISTER_OPERAND:
            reg_index   = self.IP_stream.read_byte()
            size        = self.IP_stream.read_byte()
            return self.regs[reg_index].get(size)
        elif operand_type == CONSTANT_OPERAND:
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
            try:
                self.exec()
            except ExitInterruption:
                return


def main():
    program_memory = load_memory()

    vm = VirtualMachine(program_memory)
    vm.run()


if __name__ == '__main__':
    main()
