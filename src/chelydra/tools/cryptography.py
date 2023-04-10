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

from hashlib import md5
from typing import List

def get_file_hash(absolute_path:str) -> str:
    with open(absolute_path, 'rb') as f:
        hash_obj = md5()
        hash_obj.update(f.read())
        return hash_obj.hexdigest()

def get_list_hash(data:List[str], encoding:str = 'latin1') -> str:
    hash_obj = md5()
    for chunk in sorted(data):
        hash_obj.update(chunk.encode(encoding))
    return hash_obj.hexdigest()