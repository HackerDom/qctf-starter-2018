#!/bin/bash

set -xe

dockerize -wait tcp://db:5432 -timeout 1m



case "$1" in
"manage.py")
	pushd email_confirmations
	export PYTHONPATH=..
    exec python "$@"
    ;;
"init")
	pushd email_confirmations
	export PYTHONPATH=..
	python3 manage.py db upgrade
	python3 manage.py generate_flag_owner $FLAG
	python3 manage.py generate_dummies $DUMMIES_COUNT
	popd
    ;;
"web")
	./run-with-gunicorn.sh
    ;;
*)
    exec "$@"
    ;;
esac

