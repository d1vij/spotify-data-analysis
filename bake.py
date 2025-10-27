import os
import subprocess

build_pie_path = "baked_pie.py"
sources = [
    "utils"
]

dirname = os.path.dirname(__file__)
sources = [os.path.abspath(os.path.join(dirname, path)) for path in sources]

if(not os.path.exists(build_pie_path)):
    with open(build_pie_path, "x+") as file:
        file.write("")
else:
    with open(build_pie_path, "w") as file:
        file.write("")

for path in sources:
    print(f"Current path: {path}")
    
    files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".py")]
    print(f"Files found: {len(files)}")
    
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

            with open(build_pie_path, "a") as file:


                file.write(f"# {os.path.relpath(filepath)}\n")
                file.write(content)
                file.write("\n")
                print(f"{filepath} written.")
