#!/usr/bin/env bash

set -e

if ! command -v python3 &> /dev/null; then
    echo -e "\033[31mPython is not installed on the system\033[0m"
    exit 1;
fi


if [[ ! -d ".venv" ]]; then
    echo -e "\033[32mSetting up python venv at path \"./venv\" \033[0m"
   python3 -m venv .venv

else
    echo -e "\033[32mUsing exsisting venv at path \".venv\"\033[0m"
fi

.venv/bin/python3 -m pip install -r requirements.txt
echo -e "\033[32mPython environment setup\033[0m"
source ./.venv/bin/activate
