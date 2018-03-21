#!/bin/bash

sudo apt-get update
sudo apt-get install geoip-bin -y
pip3 install -r requirements.txt --user --upgrade
