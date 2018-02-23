#!/bin/bash

./initdb.sh

chown -R www-data:www-data /var/user_data
chown -R www-data:www-data /var/tmp_user_data
chown -R www-data:www-data /var/db

./generate_users.sh
./initdb.sh

gunicorn --config gunicorn.conf.py app:app
