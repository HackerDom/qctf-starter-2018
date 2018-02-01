import struct
from abc import abstractmethod, ABC


BYTE  = 1
WORD  = 2
DWORD = 4
QWORD = 8

MEMORY_SIZE = 0xfffff

TEXT_SECTION_RANGE  = (0x00000, 0x0ffff)
BSS_SECTION_RANGE   = (0x1ffff, 0x4ffff)
STACK_SECTION_RANGE = (0x5ffff, 0xfffff)

MEMORY = ''


class Operand(ABC):
    def __init__(self, size, ptr):
        super().__init__()

        self._value = 0

    @property
    @abstractmethod
    def value(self):
        return self._value

    @value.setter
    @abstractmethod
    def value(self, nvalue):
        self._value = nvalue


class MemoryPointer(Operand):
    def __init__(self):
        super().__init__()


class NotMemoryPtr(Operand):
    def __init__(self):
        super().__init__()


class Integer(NotMemoryPtr):
    def __init__(self):
        super().__init__()


class Register(NotMemoryPtr):
    def __init__(self):
        super().__init__()


class ByteRegister(Register):
    def __init__(self):
        super().__init__()


class WordRegister(Register):
    def __init__(self):
        super().__init__()


class DwordRegister(Register):
    def __init__(self):
        super().__init__()


class QwordRegister(Register):
    def __init__(self):
        super().__init__()


class InvalidArgumentType(ValueError):
    pass


def register_memory(instruction):
    def val_reg2mem(f, s):
        if type(f) is not Register or type(s) is not MemoryPointer:
            raise InvalidArgumentType()
        instruction(f, s)
    return val_reg2mem


def register_register(instruction):
    def val_reg2reg(f, s):
        if type(f) is not Register or type(s) is not Register:
            raise InvalidArgumentType()
        instruction(f, s)
    return val_reg2reg


def memory(instruction):
    def val_mem(mem):
        if type(mem) is not MemoryPointer:
            raise InvalidArgumentType()
        instruction(mem)
    return val_mem


def register(instruction):
    def val_reg(reg):
        if type(reg) is not MemoryPointer:
            raise InvalidArgumentType()
        instruction(reg)
    return val_reg


class Assembly:
    def __init__(self):
        pass

    @register_memory
    def load(self, f: Register, s: MemoryPointer):
        pass

    @register_memory
    def store(self, f: Register, s: MemoryPointer):
        pass

    @register_register
    def add(self, f: Register, s: Register):
        pass

    @register_register
    def sub(self, f: Register, s: Register):
        pass

    @register_register
    def xor(self, f: Register, s: Register):
        pass

    @register
    def inc(self, f: Register):
        pass

    @register
    def dec(self, f: Register):
        pass

    @register_register
    def cmp(self, f: Register, s: Register):
        pass

    @memory
    def jmp(self, f: MemoryPointer):
        pass

    @memory
    def je(self, f: MemoryPointer):
        pass

    @memory
    def jg(self, f: MemoryPointer):
        pass

    @memory
    def jl(self, f: MemoryPointer):
        pass

    @register
    def hash(self, f: Register):
        pass

    @register
    def push(self, reg: Register):
        pass

    @register
    def pop(self, reg: Register):
        pass


class VirtualMachine:
    def __init__(self):
        self.init_matches()

        self.IP   = 0
        self.SP   = STACK_SECTION_RANGE[0]
        self.regs = self.init_regs()

        self.asm    = Assembly(MEMORY)

    def init_matches(self):
        self.oprdcode = {
            '\x01': ByteRegister,
            '\x02': WordRegister,
            '\x03': DwordRegister,
            '\x04': QwordRegister,
            '\x05': MemoryPointer
        }

        self.opcode = {
            '\x01': self.asm.load,
            '\x02': self.asm.store,
            '\x03': self.asm.add,
            '\x04': self.asm.sub,
            '\x05': self.asm.xor,
            '\x06': self.asm.inc,
            '\x07': self.asm.dec,
            '\x10': self.asm.cmp,
            '\x20': self.asm.jmp,
            '\x21': self.asm.je,
            '\x22': self.asm.jg,
            '\x23': self.asm.jl,
            '\x30': self.asm.hash,
            '\x50': self.asm.push,
            '\x51': self.asm.pop,
        }

    def init_regs(self):
        regs = []
        for i in range(16):
            regs.append(0)
        return regs

    def exec(self, IP):
        opcode = self.operation_codes[self.__memory[IP]]
        foper  = self.__memory[IP+1]


    @property
    def IP_byte(self):
        return self.memory[self.IP]

    def run(self):
        while self.IP_byte != 0:
            self.exec(self.IP)


def main():
    pass


if __name__ == '__main__':
    main()