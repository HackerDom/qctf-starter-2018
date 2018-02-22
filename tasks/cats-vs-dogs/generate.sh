#!/bin/bash

set -xe

tar -xf cats.tar
tar -xf dogs.tar
./generate_flags.py 400 > flags.txt
./build_images.py
rm -rf cats dogs
