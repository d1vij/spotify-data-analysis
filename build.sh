#!/usr/bin/env bash

set -e

if [[ ! -d ".venv" ]]; then
    echo -e "\033[31mNo venv found, run setup.sh first before building project\033[0m"
    exit 1
fi

echo "Executing project.ipynb notebook"
.venv/bin/python -m jupyter execute project.ipynb

echo "Converting jupyternotebook to html"
/usr/bin/env node converter.js project.ipynb "#fff" "#fff" "#fff"

echo "Converted project.ipynb to converted.html"
