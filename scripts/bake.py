import os

def readdir(root_path:str, components: list[str]):
    if (os.path.basename(root_path) == "__pycache__"):
        return
    if(os.path.isfile(root_path)):
        # What are you doing here >:(
        readfile(root_path, components)
        return
    print("Reading dir", root_path)

    for sub_path in os.listdir(root_path):
        sub_path = os.path.abspath(os.path.join(root_path, sub_path))

        if(os.path.isdir(sub_path)):
            readdir(sub_path, components)
        else:
            readfile(sub_path, components)

def readfile(sub_path: str, components:list[str]):
    with open(sub_path, "r") as file:
        print("Reading file", sub_path)

        if(os.path.basename(sub_path).split('.')[1] == "csv"):
            components.append(f"#->> {sub_path} \n\"\"\"\n{file.read()}\n\"\"\"")
        else:
            components.append(f"#->> {sub_path} \n{file.read()}")
    
def main():
    dirname = os.path.dirname(__file__)
    built_pie_path = os.path.abspath(os.path.join(dirname, "..", "built.pie"))

    roots = [
        os.path.abspath(os.path.join(dirname, "../utils")),
        # os.path.abspath(os.path.join(dirname, "../ext_data/global_music_artists.csv")),
    ]

    components: list[str] = []
    for root in roots:
        readdir(root, components) 

    with open(built_pie_path, "w+") as file:
        file.write("\n\n".join(components))
    print("Built at", built_pie_path)

if __name__ == "__main__":
    main()