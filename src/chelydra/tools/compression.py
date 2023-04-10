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

from zipfile import ZipFile

def update(compressed_file_name:str, entry_name:str, absolute_filename:str):
    with open(absolute_filename, 'rb') as fi:
        update_bytes(compressed_file_name, entry_name, fi.read())

def update_bytes(compressed_file_name:str, entry_name:str, data:bytes):
    zipfile = ZipFile(compressed_file_name, 'a')
    with zipfile.open(entry_name, 'w') as fo:
        fo.write(data)

def get_entries(compressed_file_name:str):
    zipfile = ZipFile(compressed_file_name, 'r')
    for zipinfo in zipfile.filelist:
        yield zipinfo.filename

def extract_to_folder(compressed_file_name:str, entry_name:str, folder_name:str):
    ZipFile(compressed_file_name, 'r').extract(entry_name, folder_name)