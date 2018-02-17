#!/usr/bin/python3
CSRF_ENABLED = True
SECRET_KEY = 'TODO'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
DATABASE_FILE = '/var/db/database.db'
USER_DATA_DIR = '/var/user_data' # should exist
TMP_USER_DATA_DIR = '/var/tmp_user_data' # should exist
FAKE_USERS = ['admin']
