import sys
from subprocess import Popen, PIPE, TimeoutExpired
import string

elf_path = sys.argv[1]

def is_valid_prefix(prefix):
	with Popen(elf_path, stdin=PIPE, stdout=PIPE) as p:
		p.stdin.write(prefix.encode())
		p.stdin.flush()
		try:
			p.wait(1)
		except TimeoutExpired:
			return True
		# process has finished
		out = p.stdout.read()
		return b"Ok" in out

def is_valid(flag):
	with Popen(elf_path, stdin=PIPE, stdout=PIPE) as p:
		out, err = p.communicate(flag.encode())
		return b"Ok" in out

alphabet = string.ascii_letters + string.digits + "{}"

flag = ""
while not is_valid(flag):
	for c in alphabet:
		if is_valid_prefix(flag + c):
			flag += c
			print(flag)
			break