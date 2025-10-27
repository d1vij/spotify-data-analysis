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
/usr/bin/env node converter.js project.ipynb "#fff" "#fff" "#fff"

echo "Converted project.ipynb to converted.html"
