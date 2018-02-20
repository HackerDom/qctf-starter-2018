import json
import sys
import os

def generate(filename, users_data_dir, fake_users):
    with open(filename) as f:
        users = json.load(f)

    for user in users:
        path = os.path.join(users_data_dir, user['directory'], fake_users[0])
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, 'secret.txt'), 'w') as f:
            f.write(user['flag'])

def main():
    if len(sys.argv) < 4:
        print('Usage: {} path-to-users-file users-data-dir fake-user'.format(sys.argv[0]))
        return
    generate(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
