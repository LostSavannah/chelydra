##    Chelydra. A zip-based backup and restore tool.
##    Copyright (C) 2023  Erick Fernando Mora Ramirez
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##
##    mailto:erickfernandomoraramirez@gmail.com

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

def delete_file(path:str, filename:str):
    full:str = os.sep.join([path, filename])
    if os.path.exists(full) and os.path.isfile(full):
        os.remove(full)

def empty_directory(path:str):
    for f in os.listdir(path):
        fullpath = os.sep.join([path, f])
        if os.path.isdir(fullpath):
            empty_directory(fullpath)
            os.removedirs(fullpath)
        elif os.path.isfile(fullpath):
            os.remove(fullpath)