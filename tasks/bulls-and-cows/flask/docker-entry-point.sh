#!/bin/bash

set -xe

dockerize -wait tcp://db:5432 -timeout 1m



case "$1" in
"manage.py")
	pushd bulls_and_cows
	export PYTHONPATH=..
    exec python "$@"
    ;;
"init")
	pushd bulls_and_cows
	export PYTHONPATH=..
	python3 manage.py db upgrade
	popd
    ;;
"web")
	./run-with-gunicorn.sh
    ;;
*)
    exec "$@"
    ;;
esac

