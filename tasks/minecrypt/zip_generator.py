from string import digits, ascii_letters
from random import choice, seed
from task_generator import generate

import os.path
import zipfile, io


ALPHA = digits+ascii_letters

if __name__ == "__main__":
    seed(54345)
    ids = [''.join(choice(ALPHA) for _ in range(20)) for x in range(400)]
    flags = ['QCTF{{{}}}'.format(''.join(choice(ALPHA) for _ in range(14))).upper() for x in range(400)]
    with open('ids_and_flags.py', 'w') as f:
        f.write('ids = {}\n'.format(repr(ids)))
        f.write('flags = {}'.format(repr(flags)))
    
    with open('task.py', 'r') as f:
        task_file = f.read()

    i = 0
    for id, flag in zip(ids, flags):
        i += 1
        print(i)
        encrypted = generate(flag)
        in_memory_zip = io.BytesIO()
        with zipfile.ZipFile(in_memory_zip, "a", zipfile.ZIP_DEFLATED, False) as zf:
            zf.writestr("task.py", io.BytesIO(task_file.encode()).getvalue())
            zf.writestr("encrypted.txt", io.BytesIO(encrypted.encode()).getvalue())
        with open(os.path.join('generated','{}.zip'.format(id)), 'wb') as f:
            f.write(in_memory_zip.getvalue())