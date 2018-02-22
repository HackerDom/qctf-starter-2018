#!/bin/bash
gunicorn --config gunicorn.conf.py email_confirmations.app:app
