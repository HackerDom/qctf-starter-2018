import struct
from abc import abstractmethod, ABC


BYTE  = 1
WORD  = 2
DWORD = 4

BYTEREG   = '\x50'
WORDREG   = '\x51'
DWORDREG  = '\x52'
MEMORYPTR = '\x60'
INTEGER   = '\x65'


SIZES = [BYTE, WORD, DWORD]

SIZE2FMT = {
    BYTE:  'B',
    WORD:  'H',
    DWORD: 'I',
}

MEMORY_SIZE = 0xfffff

TEXT_SECTION_RANGE  = (0x00000, 0x0ffff)
BSS_SECTION_RANGE   = (0x1ffff, 0x4ffff)
STACK_SECTION_RANGE = (0x5ffff, 0xfffff)

MEMORY = ''


def int_from_bytes(bts, size='B'):
    return struct.unpack(size, bts)[0]


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


class Operand(ABC):
    def __init__(self, size=BYTE, val=0):
        if size not in SIZES:
            raise InvalidOperandSize("You have an invalid operand size!")

        super().__init__()

        self.size  = size
        self.set_const_value(val)

    @property
    def value(self):
        return self.value

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
    def __init__(self, size=DWORD, ptr=-1):
        super().__init__(size)
        if ptr > 0:
            self.value = self.get_value(ptr)

    def get_value(self, ptr):
        return self.get_value_from_memory(ptr)

    def set_value(self, ptr, operand: Operand):
        if (TEXT_SECTION_RANGE[0] <= ptr <= TEXT_SECTION_RANGE[1]) or (BSS_SECTION_RANGE[0] <= ptr <= BSS_SECTION_RANGE[1]):
            raise PermissionException("You don't have a permission to write into .text section!")
        global MEMORY
        write_val = struct.pack(SIZE2FMT[self.size], Operand.get_value())
        MEMORY = MEMORY[:ptr] + write_val + MEMORY[ptr+self.size:]

    def get_value_from_memory(self, ptr):
        try:
            return struct.unpack(SIZE2FMT[self.size], MEMORY[ptr:ptr + self.size])[0]
        except Exception:
            raise InvalidPointerValue("Pointer is invalid.")


class NotMemoryPtr(Operand):
    def __init__(self, size, val):
        super().__init__(size, val)

    def get_value(self):
        return self.value

    def set_value(self, operand: Operand):
        write_val = operand.get_value()
        if self.size < operand.size:
            # If right operand's size is greater then left's. Like mov ax, ebx. Then we have to convert ebx to bx.
            write_val = struct.unpack(SIZE2FMT[self.size], struct.pack(SIZE2FMT[operand.size], write_val)[:self.size])
        self.value = write_val


class Integer(NotMemoryPtr):
    def __init__(self, size=DWORD, val=0):
        super().__init__(size, val)


class Register(NotMemoryPtr):
    def __init__(self, size, val=0):
        super().__init__(size, val)

    def cast(self, rtype):
        reg = rtype()
        reg.set_value(self)
        return reg


class ByteRegister(Register):
    def __init__(self, val=0):
        super().__init__(BYTE, val)


class WordRegister(ByteRegister):
    def __init__(self, val=0):
        super().__init__(WORD, val)


class DwordRegister(WordRegister):
    def __init__(self, val=0):
        super().__init__(DWORD, val)


class InvalidArgumentType(ValueError):
    pass


def register_memory(instruction):
    def val_reg2mem(f, s):
        if (not isinstance(f, Register)) or (not isinstance(s, MemoryPointer)):
            raise InvalidArgumentType()
        instruction(f, s)
    return val_reg2mem


def register_register(instruction):
    def val_reg2reg(f, s):
        if (not isinstance(f, Register)) or (not isinstance(s, Register)):
            raise InvalidArgumentType()
        instruction(f, s)
    return val_reg2reg


def memory(instruction):
    def val_mem(mem):
        if not isinstance(mem, MemoryPointer):
            raise InvalidArgumentType()
        instruction(mem)
    return val_mem


def register(instruction):
    def val_reg(reg):
        if not isinstance(reg, Register):
            raise InvalidArgumentType()
        instruction(reg)
    return val_reg


def integer(instruction):
    def val(val):
        if not isinstance(val, Integer):
            raise InvalidArgumentType()
        instruction(val)
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

    @register_memory
    def load(self, f: Register, s: MemoryPointer):
        f.set_value(s)

    @register_memory
    def store(self, f: Register, s: MemoryPointer):
        s.set_value(f)

    @register_register
    def add(self, f: Register, s: Register):
        fval = f.get_value()
        sval = s.get_value()
        f.set_value(Integer(f.size, fval + sval))

    @register_register
    def sub(self, f: Register, s: Register):
        fval = f.get_value()
        sval = s.get_value()
        f.set_value(Integer(f.size, fval - sval))

    @register_register
    def xor(self, f: Register, s: Register):
        fval = f.get_value()
        sval = s.get_value()
        f.set_value(Integer(f.size, fval ^ sval))

    @register
    def inc(self, f: Register):
        fval = f.get_value()
        f.set_value(Integer(f.size, fval + 1))

    @register
    def dec(self, f: Register):
        fval = f.get_value()
        f.set_value(Integer(f.size, fval - 1))

    @register_register
    def cmp(self, f: Register, s: Register):
        fval = f.get_value()
        sval = s.get_value()
        self.update_flags(Integer(f.size, fval - sval).get_value())

    @integer
    def jmp(self, f: Integer):
        self.IP.set_value(f)

    @integer
    def je(self, f: Integer):
        if self.FLAGS[2]:
            self.IP.set_value(f)

    @integer
    def jg(self, f: Integer):
        if self.FLAGS[1]:
            self.IP.set_value(f)

    @integer
    def jl(self, f: Integer):
        if self.FLAGS[0]:
            self.IP.set_value(f)

    @register
    def hash(self, f: Register):
        pass

    @register
    def push(self, reg: Register):
        memptr = MemoryPointer(DWORD)
        val    = reg.get_value()
        nreg   = DwordRegister(Integer(DWORD, val).get_value())
        memptr.set_value(self.SP.get_value(), nreg)
        self.SP.set_value(Integer(val=self.SP.get_value() - DWORD))

    @register
    def pop(self, reg: Register):
        memptr = MemoryPointer()
        val    = memptr.get_value(self.SP.get_value())
        reg.set_value(Integer(val=val))
        self.SP.set_value(Integer(val=self.SP.get_value() + DWORD))


class VirtualMachine:
    def __init__(self):
        self.init_matches()

        self.IP   = DwordRegister(0)
        self.SP   = DwordRegister(STACK_SECTION_RANGE[1])
        self.regs = self.init_regs()

        self.asm    = Assembly(MEMORY)

    def init_matches(self):
        self.oprdcode = {
            BYTEREG:   ByteRegister,
            WORDREG:   WordRegister,
            DWORDREG:  DwordRegister,
            MEMORYPTR: MemoryPointer,
            INTEGER:   Integer
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
            '\x40': self.asm.push,
            '\x41': self.asm.pop,
        }

        self.double_op = [self.asm.load, self.asm.store, self.asm.add,
                          self.asm.sub,  self.asm.xor,   self.asm.cmp]

        self.reg_code = [BYTEREG, WORDREG, DWORDREG]

    def init_regs(self):
        regs = []
        for i in range(16):
            regs.append(DwordRegister())
        return regs

    def get_val_size(self, IP):
        sz = MEMORY[IP+1]
        if sz not in [BYTE, WORD, DWORD]:
            raise InstructionError("Invalid value for pointer size")
        return sz

    def get_operand(self, IP):
        ptype = MEMORY[IP]
        if ptype in self.reg_code:
            num = int_from_bytes(MEMORY[IP+1])
            return self.regs[num].cast(self.oprdcode[ptype]), 2
        elif ptype == MEMORYPTR:
            ptr_sz = self.get_val_size(IP)
            ptr    = int_from_bytes(MEMORY[IP+2:IP+2+ptr_sz], SIZE2FMT[ptr_sz])
            size   = MEMORY[IP+2+ptr_sz]
            return MemoryPointer(size, ptr), 3+ptr_sz
        elif ptype == INTEGER:
            val_sz = self.get_val_size(IP)
            val    = int_from_bytes(MEMORY[IP+2:IP+2+val_sz], SIZE2FMT[val_sz])
            return Integer(val_sz, val), 3+val_sz
        else:
            raise InstructionError("Error occurred while executing an instruction")

    def exec(self, IP):
        offset = 1
        inst = self.opcode[MEMORY[IP]]
        foper, f_sz  = self.get_operand(IP + offset)

        offset += f_sz

        if inst in self.double_op:
            soper, s_sz = self.get_operand(IP + offset)
            offset += s_sz
            inst(foper, soper)
        else:
            inst(foper)
        return offset

    @property
    def IP_byte(self):
        return self.memory[self.IP.value]

    def run(self):
        while self.IP_byte != 0:
            IP_val = self.IP.value
            offset = self.exec(IP_val)
            self.IP.set_value(IP_val + offset)


def main():
    vm = VirtualMachine()
    vm.run()


if __name__ == '__main__':
    main()