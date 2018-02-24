#!/bin/bash

gunicorn --config gunicorn.conf.py app:app
