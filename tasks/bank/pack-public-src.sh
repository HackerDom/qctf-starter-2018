#!/bin/sh
cd flask
rm -f ../bank-src.zip
zip ../bank-src.zip app.py features.py model.pickle requirements.txt

