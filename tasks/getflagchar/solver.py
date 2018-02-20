import sys
from subprocess import Popen, PIPE, TimeoutExpired
import string

def is_valid_prefix(elf_path, prefix):
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

def is_valid(elf_path, flag):
	with Popen(elf_path, stdin=PIPE, stdout=PIPE) as p:
		out, err = p.communicate(flag.encode())
		return b"Ok" in out

def main():
	elf_path = sys.argv[1]

	alphabet = string.printable

	flag = ""
	while not is_valid(elf_path, flag):
		for c in alphabet:
			if is_valid_prefix(elf_path, flag + c):
				flag += c
				print(flag)
				break

if __name__ == '__main__':
	main()
