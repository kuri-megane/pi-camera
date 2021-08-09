#!/bin/bash

THIS_FILE_PATH=$(cd $(dirname $0); pwd)
cd "$THIS_FILE_PATH" || exit
python3 "$THIS_FILE_PATH"/main.py >> "$THIS_FILE_PATH"/log/stdout.txt 2>&1
