#!/bin/bash
sudo apt-get install -y  mc htop python-pip python-virtualenv arduino
sudo pip -r install flask flask-wtf

VENVDIR=./.venv/

mkdir $VENVDIR && cd $VENVDIR && virtualenv --no-site-packages --prompt="PY-VENV\n" venv

