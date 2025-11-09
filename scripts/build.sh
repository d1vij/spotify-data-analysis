#!/usr/bin/env bash

set -e

if [[ ! -d ".venv" ]]; then
    echo -e "\033[31mNo venv found, run setup.sh first before building project\033[0m"
    exit 1
fi

.venv/bin/python3 -m jupyter execute project.ipynb

echo "Baking pie"
.venv/bin/python3 bake.py

echo "Converting jupyternotebook to html"

if [[ ! command -v node ]]; then
    echo "Node is not installed!!"
    echo "It is required to convert ipynb to html"
    echo "Alternatively you can use web based converter on https://convert-ipynb.projects.divij.xyz"
    exit 1;
fi

echo "TODO FIX COLORS"
/usr/bin/env node converter.js project.ipynb "#fff" "#fff" "#fff"
echo "Converted project.ipynb to converted.html"