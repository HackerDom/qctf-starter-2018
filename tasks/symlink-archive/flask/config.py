#!/usr/bin/python3
CSRF_ENABLED = True
SECRET_KEY = 'TODO'
MAX_CONTENT_LENGTH = 1024 * 1024 # 1MB
DATABASE_FILE = '/var/db/database.db'
USER_DATA_DIR = '/var/user_data' # should exist
TMP_USER_DATA_DIR = '/var/tmp_user_data' # should exist
FAKE_USERS = ['admin']
USERS_FILE = 'users.json'
MAX_FILES_COUNT_PER_USER = 10
