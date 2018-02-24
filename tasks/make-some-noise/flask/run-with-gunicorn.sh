#!/bin/bash

gunicorn --config gunicorn.conf.py task:app
