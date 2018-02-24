#!/bin/bash

set -xe

tar -xf cats.tar
tar -xf dogs.tar
python3 generate_flags.py 400 > flags.txt
python3 build_images.py
rm -rf cats dogs
