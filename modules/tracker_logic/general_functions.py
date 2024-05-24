import json
import os


def nice_dict_(dict_: dict) -> str:
    return json.dumps(dict_, indent="\t")


def write_to_file(path: os.path, content: str) -> None:
    with open(path, "w") as file:
        json.dump(content, file, indent="\t")


def read_from_file(path: os.path) -> dict:
    with open(path, "r") as file:
        return json.load(file)
