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

import tempfile
import os
import json
import time
from typing import Dict, List
from .tools.directory import delete_file, empty_directory, get_files
from .tools.cryptography import get_file_hash, get_list_hash
from .tools.compression import extract_to_folder, update, update_bytes
from .version import VERSION_MODE_FULL, VERSION_MODE_PART, Version, VersionId

MANIFEST_NAME:str = 'manifest.json'

def get_status_from_path(path:str) -> Dict[str, str]:
    """
    Returns a Dict[str, str] which efectively represents the status of a certain
    folder. In that dictionary the key is the relative path to a file, while
    the value is the file hash
    """
    offset = len(path) + len(os.sep)
    return {i[offset:]:get_file_hash(i) for i in get_files(path)}

def get_manifest_name(path:str) -> str:
    """
    Returns a string which represents how should the manifest get called in a 
    certain path
    """
    return os.sep.join([path, MANIFEST_NAME])

def save_manifest(path:str, content):
    f"""
    Saves the content as a {MANIFEST_NAME} in the specified path
    """
    if not os.path.exists(path):
        raise Exception(f"Path {path} doesn't exists")
    with open(get_manifest_name(path), 'w') as fo:
        json.dump(content, fo, indent='\t')

def get_manifest(path:str):
    """
    Retrieves the manifest content as a object
    """
    if not os.path.exists(get_manifest_name(path)):
        save_manifest(path, {"versions":[]})
    with open(get_manifest_name(path), 'r') as fi:
        return json.load(fi)

def get_restore_order(path:str, epoch:float = None) -> List[Version]:
    """
    Retrieves the collection which represents the restore order based in 
    a moment in time from a certain version until that specified moment.
    If there's a FULL backup somewhere before that moment, then it returns
    every version from that FULL backup until the specified epoch.
    """
    epoch = epoch or time.time()
    current_manifest = get_manifest(path)
    past = [v for v in current_manifest['versions'] if v['epoch'] < epoch]
    past = sorted(past, key=lambda v: v['epoch'], reverse=True)
    backtrack = []
    for version in past:
        backtrack.append(version)
        if version['mode'] == VERSION_MODE_FULL:
            break
    while len(backtrack) > 0:
        version_object = Version().load(backtrack.pop())
        yield version_object

def get_status_from_backup(path:str, epoch:float = None):
    """
    Returns the current status as is in the backup history.
    """
    status = {}
    for version in get_restore_order(path, epoch):
        for change in version.changes:
            status[change] = version.changes[change]
        for deletion in version.deletions:
            del status[deletion]
    return status

def create_version(source:str, backup:str, full:bool = False) -> bool:
    """
    Creates a version. If full is true, it will create a full version and 
    return true. Otherwise it will try to create a partial version depending on
    if there were any changes.  
    """
    current_status = get_status_from_path(source)
    current_manifest = get_manifest(backup)
    deletions = []
    mode = VERSION_MODE_FULL if full else VERSION_MODE_PART
    order = len(current_manifest['versions']) + 1
    if not full:
        changes = {}
        backup_status = get_status_from_backup(backup)
        deletions = [f for f in backup_status if f not in current_status]
        for f in current_status:
            if f not in backup_status or backup_status[f] != current_status[f]:
                changes[f] = current_status[f]            
        if len(changes) == 0 and len(deletions) == 0:
            return False
        current_status = changes
    code = get_list_hash([i for i in current_status.values()])
    epoch = time.time()
    id = VersionId(mode, code, epoch, order)
    compile_version(Version(id, current_status, deletions), source, backup)
    return True

def compile_version(version:Version, source:str, backup:str):
    """
    Efectively creates the version in disk. That means than it creates the
    compressed archive with the version specs and updates the manifest
    """
    filename = version.get_filename('.zip')
    full_filename = os.sep.join([backup, filename])
    for change in version.changes:
        change_file = os.sep.join([source, change])
        update(full_filename, change, change_file)
    else:
        content = json.dumps(version.get_dict()).encode('latin1')
        filename = f'{version.id.code}.json'
        update_bytes(full_filename, filename, content)
    current_manifest = get_manifest(backup)
    current_manifest['versions'].append(version.get_dict())
    save_manifest(backup, current_manifest)

def restore_into(backup:str, target:str, till_epoch:float = None, empty_target:bool = False):
    if not os.path.exists(target):
        os.makedirs(target)
    elif os.path.isfile(target):
        raise Exception(f"Can't restore into file: {target}")
    files:Dict[str, Version] = {}
    deletions:List[str] = []
    for version in get_restore_order(backup, till_epoch):
        for file in version.changes:
            files[file] = version
            if file in deletions:
                deletions.remove(file)
        for deletion in version.deletions:
            del files[deletion]
            if deletion not in deletions:
                deletions.append(deletion)
    if empty_target:
        empty_directory(target)
    for entry in files:
        compressed_file_name = files[entry].get_filename('.zip')
        fullname = os.sep.join([backup, compressed_file_name])
        extract_to_folder(fullname, entry, target)
    for deletion in deletions:
        delete_file(target, deletion)

def syncronize(folders:List[str], source:str, backup:str):
    if create_version(source, backup):
        for target in folders:
            if target == source:
                continue
            restore_into(backup, target, empty_target=True)