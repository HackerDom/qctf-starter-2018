import os
from ids_generator import task_ids, pins, flags
from subprocess import Popen, PIPE
from time import sleep

PACKAGE_PATH = "./generated/"
GENERATOR = "task_generator.py"
BINARY_NAME = "protected.exe"


def is_valid(task_file, pin, flag):
    with Popen(task_file, stdin=PIPE, stdout=PIPE) as p:
        p.stdin.write(pin.encode() + b"\n")
        p.stdin.flush()
        sleep(1)
        p.stdin.write(flag.encode() + b"\n")
        p.stdin.flush()
        out, err = p.communicate()
        return b"right" in out


def main():
    for team_id, task_id in enumerate(task_ids):
        print("Generating task for team", team_id)

        pin = pins[team_id]
        flag = flags[team_id]
        
        task_folder = os.path.join(PACKAGE_PATH, task_id)
        os.makedirs(task_folder, exist_ok=True)
        
        task_file = os.path.join(task_folder, BINARY_NAME)
        
        os.system("python3 {} {} {} {}".format(GENERATOR, pin, flag, task_file))

        assert is_valid(task_file, pin, flag)


if __name__ == '__main__':
    main()