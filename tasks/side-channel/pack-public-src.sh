#!/bin/bash

mv app.py{,.private}
sed -e "s/PASSWORD = .*$/PASSWORD = '**********'/g" \
    -e 's/QCTF{.*}/QCTF{********************}/g' app.py.private > app.py

zip public-src.zip app.py mnist_cnn.h5 requirements.txt

mv app.py{.private,}
