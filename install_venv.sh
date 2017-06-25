#!/usr/bin/env bash

install_dir=$1
git clone https://github.com/paudan/pynlp-sandbox.git
virtualenv $install_dir
$install_dir/bin/pip3 install -r requirements.txt
pyb -P install_dir=$install_dir
