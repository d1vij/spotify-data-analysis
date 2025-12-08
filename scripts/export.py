import subprocess

if __name__ == "__main__":
    subprocess.run(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            "--no-prompt",
            "project.ipynb",
            "--output", "index.html"
        ],
        cwd=".",
    )
