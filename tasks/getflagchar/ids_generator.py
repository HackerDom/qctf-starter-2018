from hashlib import md5

TEAMS_COUNT = 450

def gen_task_id(team_id):
	return md5(b"UYF2v976_R$^!F^@FGW*^$DQFWCjyrdhgj%d" % team_id).hexdigest()

def gen_flag(team_id):
	return "QCTF{%s}" % md5(b"bjhgyT^FR&Kv23F$Y#$UIfg2MsfgVE#SDY?DJY%d" % team_id).hexdigest()

task_ids = [gen_task_id(team_id) for team_id in range(TEAMS_COUNT)]
flags = [gen_flag(team_id) for team_id in range(TEAMS_COUNT)]

def main():
	print(repr(task_ids))
	print(repr(flags))

if __name__ == '__main__':
	main()
