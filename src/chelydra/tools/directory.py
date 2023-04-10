import os
from typing import List

def get_directories(path:str, ignore:List[str] = None, current:str = None):
    ignore = ignore or []
    current = current or path
    for folder in os.listdir(path):
        if folder in ignore:
            continue
        next_path = os.sep.join([path, folder])
        yield next_path
        if os.path.isdir(next_path):
            for sub in get_directories(next_path, ignore, folder):
                yield sub

def get_folders(path, ignore:List[str] = None):
    for directory in get_directories(path, ignore):
        if os.path.isdir(directory):
            yield directory

def get_files(path, ignore:List[str] = None):
    for directory in get_directories(path, ignore):
        if os.path.isfile(directory):
            yield directory