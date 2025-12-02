# Compiles all the source-code into a single file, essentially "baking" the pie

import os

# kuchi puhh
ignore = ["__pycache__", ".ipynb_checkpoints"]


def read_dir(root_path: str, components: list[str]):
    if os.path.basename(root_path) in ignore:
        return
    if os.path.isfile(root_path):
        # What are you doing here >:(
        read_file(root_path, components)
        return
    print("Reading dir", root_path)

    for sub_path in os.listdir(root_path):
        sub_path = os.path.abspath(os.path.join(root_path, sub_path))

        if os.path.isdir(sub_path):
            read_dir(sub_path, components)
        else:
            read_file(sub_path, components)


def read_file(sub_path: str, components: list[str]):
    if os.path.basename(sub_path) in ignore:
        return
    with open(sub_path, "r") as file:
        print("Reading file", sub_path)

        if os.path.basename(sub_path).split(".")[1] != "py":
            # Paste as multiline comment if the file is not a python file
            components.append(f"# {sub_path} ".center(80, "#"))
            components.append(f'"""\n{file.read()}\n"""')
        else:
            components.append(f"# {sub_path} ".center(80, "#"))
            components.append(f"\n{file.read()}\n")


def main():
    dirname = os.path.dirname(__file__)
    built_pie_path = os.path.abspath(os.path.join(dirname, "..", "build", "built.pie"))

    roots = [
        os.path.abspath(os.path.join(dirname, "../utils")),
        os.path.abspath(os.path.join(dirname, "../scripts")),
        # os.path.abspath(os.path.join(dirname, "../ext_data/global_music_artists.csv")), # Too big lmao
    ]

    components: list[str] = []

    # Having the magic functions in here allows for re-pasting of source code without rewriting all the magic commands :)
    components.append("%%capture\n# ^Catch all the output of this cell")
    components.append("# Run the script to compile all python files\n%run ./scripts/bake.py")
    components.append("# Paste the content of the compiled file into this cell\n%loadnext ./build/built.pie")
    components.append("# This raises error but also prevents running this cell :)\nraise SystemError\n")
    for root in roots:
        read_dir(root, components)

    with open(built_pie_path, "w+") as file:
        file.write("\n\n".join(components))
    print("Built at", built_pie_path)


if __name__ == "__main__":
    main()
