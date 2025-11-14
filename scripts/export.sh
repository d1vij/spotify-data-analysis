#!/usr/bin/env bash
.venv/bin/python3 -m jupyter nbconvert --to html --no-prompt project.ipynb --output-dir="./build"
