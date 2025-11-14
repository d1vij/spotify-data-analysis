import subprocess

# .venv/bin/python3 -m jupyter nbconvert --to html --no-prompt project.ipynb --output-dir="./build"


if (__name__ == "__main__"):
    subprocess.run(["jupyter", "nbconvert", "--to", "html", "--no-prompt", "project.ipynb", "--output-dir=\"./build\""], cwd=".")