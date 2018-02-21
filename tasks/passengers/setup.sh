#!/usr/bin/env bash
sudo cp ./passengers.xinetd /etc/xinetd.d/passengers
sudo service xinetd reload