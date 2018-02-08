##!/usr/bin/python3

import struct

from abc import abstractmethod, ABC
from functools import wraps


BYTE  = 1
WORD  = 2
DWORD = 4

BYTEREG   = '\x50'
WORDREG   = '\x51'
DWORDREG  = '\x52'
MEMORYPTR = '\x60'
INTEGER   = '\x65'

NULLBYTE = '\x00'

SIZES = [BYTE, WORD, DWORD]

SIZE2FMT = {
    BYTE:  'b',
    WORD:  'h',
    DWORD: 'i',
}

MEMORY_SIZE = 0x6000

TEXT_SECTION_RANGE  = (0x0000, 0x0fff)
HEAP_SECTION_RANGE  = (0x1fff, 0x2fff)
STACK_SECTION_RANGE = (0x3fff, 0x5fff)

MEMORY = ""


def int_from_bytes(bts, size='B'):
    return struct.unpack(size, bytes([ord(x) for x in bts]))[0]


def load_memory():
    global MEMORY
    with open('memory', 'r') as mem:
        MEMORY = mem.read()


class InvalidOperandPointer(Exception):
    pass


class PermissionException(Exception):
    pass


class InvalidPointerValue(Exception):
    pass


class InvalidOperandSize(Exception):
    pass


class InvalidValueSize(Exception):
    pass


class InstructionError(Exception):
    pass


class StackRangeCorrupted(Exception):
    pass


class Operand(ABC):
    def __init__(self, val=0, size=BYTE):
        if size not in SIZES:
            raise InvalidOperandSize("You have an invalid operand size!")

        super().__init__()

        self.size  = size
        self.set_const_value(val)

    @abstractmethod
    def get_value(self, *args):
        pass

    @abstractmethod
    def set_value(self, *args):
        pass

    def set_const_value(self, val):
        self.value = 0
        try:
            struct.pack(SIZE2FMT[self.size], val)
            self.value = val
        except Exception:
            raise InvalidValueSize("Size of specified value is greater than Integer's size")


class MemoryPointer(Operand):
    def __init__(self, ptr, size=DWORD):
        super().__init__(size=size)

        self.ptr   = ptr
        self.value = self.get_value()

    def get_value(self):
        try:
            return struct.unpack(SIZE2FMT[self.size], MEMORY[self.ptr:self.ptr + self.size].encode())[0]
        except Exception:
            raise InvalidPointerValue("Pointer is invalid.")

    def set_value(self, operand: Operand):
        if (TEXT_SECTION_RANGE[0] <= self.ptr <= TEXT_SECTION_RANGE[1]):
            raise PermissionException("You don't have a permission to write into .text section!")
        global MEMORY
        write_val = struct.pack(SIZE2FMT[self.size], operand.get_value()).decode('unicode_escape')
        MEMORY = MEMORY[:self.ptr] + write_val + MEMORY[self.ptr+self.size:]


class NotMemoryPtr(Operand):
    def __init__(self, val, size):
        super().__init__(val, size)

    def get_value(self):
        return self.value

    def set_value(self, operand: Operand):
        write_val = operand.get_value()
        if self.size < operand.size:
            # If right operand's size is greater then left's. Like mov ax, ebx. Then we have to convert ebx to bx.
            write_val = struct.unpack(SIZE2FMT[self.size], struct.pack(SIZE2FMT[operand.size], write_val)[:self.size])[0]
        self.value = write_val


class Integer(NotMemoryPtr):
    def __init__(self, val=0, size=DWORD):
        super().__init__(val, size)


class Register(NotMemoryPtr):
    def __init__(self, val=0, size=DWORD):
        super().__init__(val, size)

    def cast(self, rtype):
        reg = rtype()
        reg.set_value(self)
        self.set_value(reg)

    def deref(self):
        return MemoryPointer(self.value, self.size)


class ByteRegister(Register):
    def __init__(self, val=0):
        super().__init__(val, BYTE)


class WordRegister(Register):
    def __init__(self, val=0):
        super().__init__(val, WORD)


class DwordRegister(Register):
    def __init__(self, val=0):
        super().__init__(val, DWORD)


class InvalidArgumentType(ValueError):
    pass


def try2invoke(*args, count=1):
    if count == 1:
        if not isinstance(args[1], args[2]):
            raise InvalidArgumentType()
        args[3](args[0], args[1])
    else:
        if (not isinstance(args[1], args[2])) or (not isinstance(args[3], args[4])):
            raise InvalidArgumentType()
        args[5](args[0], args[1], args[3])


def register_operand(instruction):
    @wraps(instruction)
    def val_reg2opr(self, f, s):
        try2invoke(self, f, Register, s, Operand, instruction, count=2)
    return val_reg2opr


def register_memory(instruction):
    @wraps(instruction)
    def val_reg2mem(self, f, s):
        try2invoke(self, f, Register, s, MemoryPointer, instruction, count=2)
    return val_reg2mem


def register_register(instruction):
    @wraps(instruction)
    def val_reg2reg(self, f, s):
        try2invoke(self, f, Register, s, Register, instruction, count=2)
    return val_reg2reg


def memory(instruction):
    @wraps(instruction)
    def val_mem(self, mem):
        try2invoke(self, mem, MemoryPointer, instruction)
    return val_mem


def register(instruction):
    @wraps(instruction)
    def val_reg(self, reg):
        try2invoke(self, reg, Register, instruction)
    return val_reg


def integer(instruction):
    @wraps(instruction)
    def val(self, val):
        try2invoke(self, val, Integer, instruction)
    return val


class Assembly:
    def __init__(self, IP: DwordRegister, SP: DwordRegister):
        self.IP = IP
        self.SP = SP
        self.FLAGS = [0, 0, 0] # Is Less [IL], Is Greater [IG], Is Equal [IE]

    def update_flags(self, val):
        if val == 0:
            self.FLAGS[2] = 1
        elif val < 0:
            self.FLAGS[0] = 1
        else:
            self.FLAGS[1] = 1

    def clear_flags(self):
        self.FLAGS = [0, 0, 0]

    @register_operand
    def load(self, f: Register, s: Operand):
        f.set_value(s)

    @register_memory
    def store(self, f: Register, s: MemoryPointer):
        s.set_value(f)

    @register_operand
    def add(self, f: Register, s: Operand):
        fval = f.get_value()
        sval = s.get_value()
        f.set_value(Integer(fval + sval, f.size))

    @register_operand
    def sub(self, f: Register, s: Operand):
        fval = f.get_value()
        sval = s.get_value()
        f.set_value(Integer(fval - sval, f.size))

    @register_operand
    def xor(self, f: Register, s: Operand):
        fval = f.get_value()
        sval = s.get_value()
        f.set_value(Integer(fval ^ sval, f.size))

    @register
    def inc(self, f: Register):
        fval = f.get_value()
        f.set_value(Integer(fval + 1, f.size))

    @register
    def dec(self, f: Register):
        fval = f.get_value()
        f.set_value(Integer(fval - 1, f.size))

    @register_register
    def cmp(self, f: Register, s: Register):
        fval = f.get_value()
        sval = s.get_value()
        self.update_flags(Integer(fval - sval, f.size).get_value())

    @integer
    def jmp(self, f: Integer):
        self.IP.set_value(f)

    @integer
    def je(self, f: Integer):
        if self.FLAGS[2]:
            self.jmp(f)
            self.clear_flags()

    @integer
    def jg(self, f: Integer):
        if self.FLAGS[1]:
            self.jmp(f)
            self.clear_flags()

    @integer
    def jl(self, f: Integer):
        if self.FLAGS[0]:
            self.jmp(f)
            self.clear_flags()

    @register
    def hash(self, f: Register):
        pass

    @register
    def puts(self, f: Register):
        buf, ptr = '', f.get_value()
        while MEMORY[ptr] != NULLBYTE:
            buf += MEMORY[ptr]
            ptr += 1
        print(buf)

    @register
    def gets(self, f: Register, msg: str = "Enter a string: "):
        global MEMORY
        buf, ptr = input(msg), f.get_value()
        MEMORY = MEMORY[:ptr] + buf + MEMORY[ptr + len(buf):]

    @register
    def push(self, reg: Register):
        if self.SP.get_value() <= STACK_SECTION_RANGE[0]:
            raise StackRangeCorrupted("Pushing is happening when the stack is full.")
        self.SP.set_value(Integer(val=self.SP.get_value() - DWORD))
        memptr = MemoryPointer(self.SP.get_value(), DWORD)
        nreg   = reg.cast(DwordRegister)
        memptr.set_value(nreg)

    @register
    def pop(self, reg: Register):
        if self.SP.get_value() >= STACK_SECTION_RANGE[1]:
            raise StackRangeCorrupted("Pop is happening when the stack is empty!")
        memptr = MemoryPointer(self.SP.get_value(), DWORD)
        reg.set_value(memptr)
        self.SP.set_value(Integer(val=self.SP.get_value() + DWORD))

    def exit(self):
        pass


class VirtualMachine:
    def __init__(self):
        self.IP   = DwordRegister(0)
        self.SP   = DwordRegister(STACK_SECTION_RANGE[1])
        self.regs = self.init_regs()

        self.asm  = Assembly(self.IP, self.SP)

        self.init_matches()

    def init_matches(self):
        self.oprdcode = {
            BYTEREG:   ByteRegister,
            WORDREG:   WordRegister,
            DWORDREG:  DwordRegister,
            MEMORYPTR: MemoryPointer,
            INTEGER:   Integer
        }

        self.opcode = {
            '\x11': self.asm.load,
            '\x12': self.asm.store,
            '\x13': self.asm.add,
            '\x14': self.asm.sub,
            '\x15': self.asm.xor,
            '\x16': self.asm.inc,
            '\x17': self.asm.dec,
            '\x20': self.asm.cmp,
            '\x30': self.asm.jmp,
            '\x31': self.asm.je,
            '\x32': self.asm.jg,
            '\x33': self.asm.jl,
            '\x40': self.asm.hash,
            '\x41': self.asm.puts,
            '\x42': self.asm.gets,
            '\x25': self.asm.push,
            '\x26': self.asm.pop,
            '\x00': self.asm.exit
        }

        self.double_op = [self.asm.load, self.asm.store, self.asm.add,
                          self.asm.sub,  self.asm.xor,   self.asm.cmp]

        self.reg_code = [BYTEREG, WORDREG, DWORDREG]

    def init_regs(self):
        regs = []
        for i in range(16):
            regs.append(DwordRegister())
        return regs

    def add2IP(self, offset):
        val = self.IP.get_value()
        self.IP.set_value(Integer(val=(val+offset)))

    def get_val_size(self, IP):
        sz = int_from_bytes(MEMORY[IP+1])
        if sz not in [BYTE, WORD, DWORD]:
            raise InstructionError("Invalid value for pointer size")
        return sz

    def get_operand(self, IP):
        ptype = MEMORY[IP]
        if ptype in self.reg_code:
            num   = int_from_bytes(MEMORY[IP+1])
            deref = int_from_bytes(MEMORY[IP+2])
            self.regs[num].cast(self.oprdcode[ptype])
            return (self.regs[num].deref() if deref else self.regs[num]), 3
        elif ptype == MEMORYPTR:
            ptr_sz = self.get_val_size(IP)
            ptr    = int_from_bytes(MEMORY[IP+2:IP+2+ptr_sz], SIZE2FMT[ptr_sz])
            size   = MEMORY[IP+2+ptr_sz]
            return MemoryPointer(ptr, size), 3+ptr_sz
        elif ptype == INTEGER:
            val_sz = self.get_val_size(IP)
            val    = int_from_bytes(MEMORY[IP+2:IP+2+val_sz], SIZE2FMT[val_sz])
            return Integer(val, val_sz), 2+val_sz
        else:
            raise InstructionError("Error occurred while executing an instruction")

    def exec(self, IP):
        offset, oprs = 1, ()
        inst = self.opcode[MEMORY[IP]]
        foper, f_sz  = self.get_operand(IP + offset)

        offset += f_sz

        if inst in self.double_op:
            soper, s_sz = self.get_operand(IP + offset)
            offset += s_sz
            oprs = (foper, soper)
        else:
            oprs = (foper,)
        self.add2IP(offset)
        inst(*oprs)

    @property
    def IP_byte(self):
        return MEMORY[self.IP.get_value()]

    def run(self):
        while self.IP_byte != NULLBYTE:
            IP_val = self.IP.get_value()
            self.exec(IP_val)


def main():
    load_memory()

    vm = VirtualMachine()
    vm.run()


if __name__ == '__main__':
    main()