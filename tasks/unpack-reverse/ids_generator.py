from hashlib import md5
import random

TEAMS_COUNT = 450

def gen_task_id(team_id):
	return md5(b"JFdwchjhEkd53tcvu$#&*HRjgFD212we%d" % team_id).hexdigest()

def gen_pin(team_id):
	random.seed(team_id + 73313)
	return str(random.randint(10**15, 10**17))

def gen_flag(team_id):
	return "QCTF{%s}" % md5(b",mnB*TREdsja2sycfg4c3cc45Whge.h&*#y%d" % team_id).hexdigest()

task_ids = [gen_task_id(team_id) for team_id in range(TEAMS_COUNT)]
pins = [gen_pin(team_id) for team_id in range(TEAMS_COUNT)]
flags = [gen_flag(team_id) for team_id in range(TEAMS_COUNT)]

def main():
	print(repr(task_ids))
	print(repr(flags))

if __name__ == '__main__':
	main()