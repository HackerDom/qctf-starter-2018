import os
import re
import hashlib
import zipfile

import goldreich


def getenv(name):
    value = os.getenv(name)
    if value is None:
        raise ValueError(f'Please provide a value for the environment variable {name}')
    return value


TEMPLATE_SEED = b'substitutethis'

PYC_TEMPLATE = 'goldreich.cpython-36.pyc'
PATCH = '0001.patch'
OUTPUT_DIR = 'team_files'
INDEX = os.path.join(OUTPUT_DIR, 'index.txt')
TEAM_COUNT = 600
SECRET = getenv('SECRET')


def generate_archive(archive_path, pyc_template, seed, pyc_archive_name, patch_path):
    seed_index = re.search(TEMPLATE_SEED, pyc_template).start()
    pyc_contents = pyc_template[:seed_index] + seed.encode('utf-8') + pyc_template[seed_index + len(TEMPLATE_SEED):]

    with zipfile.ZipFile(archive_path, 'w') as archive:
        archive.write(patch_path)
        archive.writestr(pyc_archive_name, pyc_contents)



def main(pyc_template_path, patch_path, output_dir, index_path, team_count, secret):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    with open(pyc_template_path, 'rb') as f:
        pyc_template = f.read()

    flags = {}
    archive_names = {}
    for team_number in range(1, team_count + 1):
        seed_hash = hashlib.sha256(f'{secret}_{team_number}_seed'.encode('utf-8')).hexdigest()
        seed = seed_hash[: len(TEMPLATE_SEED)]

        archive_name_hash = hashlib.sha256(f'{secret}_{team_number}_seed'.encode('utf-8')).hexdigest()
        archive_name = f'{team_number}-{archive_name_hash:.10}.zip'
        archive_path = os.path.join(output_dir, archive_name)

        flags[team_number] = goldreich.main(seed)
        archive_names[team_number] = archive_name
        generate_archive(archive_path, pyc_template, seed, pyc_template_path, patch_path)

    with open(index_path, 'w') as f:
        for team_number in sorted(flags.keys()):
            f.write(f'{team_number}\t{archive_names[team_number]}\t{flags[team_number]}\n')


if __name__ == '__main__':
    main(PYC_TEMPLATE, PATCH, OUTPUT_DIR, INDEX, TEAM_COUNT, SECRET)
