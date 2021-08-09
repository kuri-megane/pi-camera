#!/bin/bash

THIS_FILE_PATH=$(cd $(dirname $0); pwd)
cd "$THIS_FILE_PATH" || exit
/usr/bin/python3 "$THIS_FILE_PATH"/main.py
