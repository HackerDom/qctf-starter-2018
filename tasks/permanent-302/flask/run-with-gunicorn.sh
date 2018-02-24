#!/bin/bash

gunicorn --config gunicorn.conf.py permanent-302:app
