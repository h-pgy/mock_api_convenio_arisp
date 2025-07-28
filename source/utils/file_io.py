import os
import json


def create_directory_if_not_exists(directory_path)->str:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return os.path.abspath(directory_path)


def solve_path(file_path:str, parent_directory=None)->str:

    if parent_directory:
        return os.path.join(parent_directory, file_path)
    return file_path

def get_file(file_name:str, parent_directory=None, raise_if_not_exists:bool=True)->str:

    if parent_directory:
        file_path = os.path.join(parent_directory, file_name)
    else:
        file_path = os.path.abspath(file_name)
    if not os.path.exists(file_path) and raise_if_not_exists:
        raise ValueError(f"The file {file_path} does not exist.")
    return file_path


def read_binary_file(file_name:str, parent_directory=None) -> bytes:

    file = get_file(file_name, parent_directory)
    with open(file, 'rb') as file:
        return file.read()
    
def read_json_file(file_name, parent_directory=None) -> dict:

    file = get_file(file_name, parent_directory)
    with open(file, 'r') as file:
        return json.load(file)
    
def save_json_file(data: dict, file_name: str, parent_directory=None) -> None:
    
    file_path = get_file(file_name, parent_directory)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

