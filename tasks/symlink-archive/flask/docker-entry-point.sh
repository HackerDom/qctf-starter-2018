#!/bin/bash

set -xe

chown -R www-data:www-data /var/user_data
chown -R www-data:www-data /var/tmp_user_data
chown -R www-data:www-data /var/db

./generate_users.sh

case "$1" in
"init")
	rm -rf /var/db/*
	./initdb.sh
    ;;
"web")
	./run-with-gunicorn.sh
    ;;
*)
    exec "$@"
    ;;
esac


