#!/bin/bash

set -xe

dockerize -wait tcp://db:3306 -timeout 1m

case "$1" in
"init")
	python3 db_adjustment.py
    ;;
"web")
	./run.sh
    ;;
*)
    exec "$@"
    ;;
esac
