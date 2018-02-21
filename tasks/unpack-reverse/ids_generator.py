from hashlib import md5

def gen_task_id(team_id):
	return md5(b"JFdwchjhEkd53tcvu$#&*HRjgFD212we%d" % team_id).hexdigest()

def gen_flag(team_id):
	return "QCTF{%s}" % md5(b",mnB*TREdsja2sycfg4c3cc45Whge.h&*#y%d" % team_id).hexdigest()

task_ids = [gen_task_id(team_id) for team_id in range(400)]
flags = [gen_flag(team_id) for team_id in range(400)]

def main():
	print(repr(task_ids))
	print(repr(flags))

if __name__ == '__main__':
	main()