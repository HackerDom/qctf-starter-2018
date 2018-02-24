#!/bin/bash
gunicorn --config gunicorn.conf.py bulls_and_cows.app:app
