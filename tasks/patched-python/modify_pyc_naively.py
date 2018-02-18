import os
import sys
import re
import py_compile


CALL_FUNCTION_TEMPLATE = re.compile(b'(\x83\x01)+')
CALL_UNARY_FUNCTIONS_OPCODE = 200
NOP_OPCODE = 9
ROT_TWO_OPCODE = 2
ROT_THREE_OPCODE = 3

NOP_INSTRUCTION = [NOP_OPCODE, NOP_OPCODE]
ROT_TWO_INSTRUCTION = [ROT_TWO_OPCODE, 0]
ROT_THREE_INSTRUCTION = [ROT_THREE_OPCODE, 0]


def generate_compex_nops(byte_count):
    if byte_count % 2 != 0:
        raise ValueError('Cannot generate instructions for an odd number of bytes')

    instruction_count = byte_count // 2

    if instruction_count < 2:
        return NOP_INSTRUCTION * instruction_count
    elif instruction_count % 2 == 0:
        return ROT_TWO_INSTRUCTION * instruction_count
    else:
        return ROT_THREE_INSTRUCTION * 3 + ROT_TWO_INSTRUCTION * (instruction_count - 3)


def modify(bytecode):
    result = bytearray(bytecode)
    for match in CALL_FUNCTION_TEMPLATE.finditer(bytecode):
        first_index = match.start()
        argument_count = (match.end() - match.start()) // 2
        result[first_index] = CALL_UNARY_FUNCTIONS_OPCODE
        result[first_index + 1] = argument_count
        result[first_index + 2: match.end()] = generate_compex_nops(match.end() - first_index - 2)

    return bytes(result)


def main(source_path):
    script_name, _ = os.path.splitext(source_path)
    original_pyc_name = f'{script_name}_original.cpython-36.pyc'
    modified_pyc_name = f'{script_name}.cpython-36.pyc'
    py_compile.compile(source_path, original_pyc_name)
    with open(original_pyc_name, 'rb') as f:
        bytecode = f.read()
    modified_bytecode = modify(bytecode)
    with open(modified_pyc_name, 'wb') as f:
        f.write(modified_bytecode)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} script.py', file=sys.stderr)

    main(sys.argv[1])
