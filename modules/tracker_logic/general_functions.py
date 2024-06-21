import json
import os


def nice_dict_(dict_: dict) -> str:
    return json.dumps(dict_, indent="\t")


def write_to_file(path: os.path, content) -> None:
    with open(path, "w") as file:
        json.dump(content, file, indent="\t")


def read_from_file(path: os.path) -> dict:
    with open(path, "r") as file:
        return json.load(file)
    
def get_file_name(path : os.path) -> str:
    file_name_with_extension = os.path.basename(path)

    file_name, _ = os.path.splitext(file_name_with_extension)

    return file_name