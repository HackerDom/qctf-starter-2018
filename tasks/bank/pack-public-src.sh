#!/bin/sh
cd flask
rm -f ../public-src.zip
zip ../public-src.zip app.py features.py model.pickle requirements.txt

