import os
from ids_generator import task_ids, flags
from solver import is_valid

PACKAGE_PATH = "./generated/"
GENERATOR = "task_generator.py"

def main():
	for team_id, task_id in enumerate(task_ids):
		print("Generating task for team" , team_id)

		flag = flags[team_id]
		
		task_folder = os.path.join(PACKAGE_PATH, task_id)
		os.makedirs(task_folder, exist_ok=True)
		
		task_file = os.path.join(task_folder, "scanner")
		
		os.system("python3 {} {} {}".format(GENERATOR, flag, task_file))

		assert is_valid(task_file, flag)


if __name__ == '__main__':
	main()
