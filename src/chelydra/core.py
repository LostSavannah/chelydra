import os
import json
import time
from typing import Dict, List
from .tools.directory import get_files
from .tools.cryptography import get_file_hash, get_list_hash
from .tools.compression import update, update_bytes
from .version import VERSION_MODE_FULL, VERSION_MODE_PART, Version, VersionId

MANIFEST_NAME:str = 'manifest.json'

def get_status_from_path(path:str) -> Dict[str, str]:
    offset = len(path) + len(os.sep)
    return {i[offset:]:get_file_hash(i) for i in get_files(path)}

def get_manifest_name(path:str) -> str:
    return os.sep.join([path, MANIFEST_NAME])

def save_manifest(path:str, content):
    if not os.path.exists(path):
        raise Exception(f"Path {path} doesn't exists")
    with open(get_manifest_name(path), 'w') as fo:
        json.dump(content, fo, indent='\t')

def get_manifest(path:str):
    if not os.path.exists(get_manifest_name(path)):
        save_manifest(path, {"versions":[]})
    with open(get_manifest_name(path), 'r') as fi:
        return json.load(fi)

def get_restore_order(path:str, epoch:float = None) -> List[Version]:
    epoch = epoch or time.time()
    current_manifest = get_manifest(path)
    past = [v for v in current_manifest['versions'] if v['epoch'] < epoch]
    backtrack = sorted(past, key=lambda v: v['epoch'])
    backtrack.reverse()
    for version in backtrack:
        version_object = Version().load(version)
        yield version_object
        if version_object.is_full():
            break

def get_status_from_backup(path:str, epoch:float = None):
    status = {}
    for version in get_restore_order(path, epoch):
        for deletion in version.deletions:
            del status[deletion]
        for change in version.changes:
            status[change] = version.changes[change]
    return status

def create_full_version(source:str, backup:str) -> bool:
    current_status = get_status_from_path(source)
    current_manifest = get_manifest(backup)
    code = get_list_hash([i for i in current_status.values()])
    mode = VERSION_MODE_FULL
    epoch = time.time()
    order = len(current_manifest['versions']) + 1
    id = VersionId(mode, code, epoch, order)
    compile_version(Version(id, current_status, []), source, backup)
    return True

def create_partial_version(source:str, backup:str) -> bool:
    current_status = get_status_from_path(source)
    current_manifest = get_manifest(backup)
    backup_status = get_status_from_backup(backup)
    changes = {}
    deletions = [f for f in backup_status if f not in current_status]
    for f in current_status:
        if f not in backup_status or backup_status[f] != current_status[f]:
            changes[f] = current_status[f]            
    if len(changes) == 0 and len(deletions) == 0:
        return False
    code = get_list_hash([i for i in changes.values()])
    mode = VERSION_MODE_PART
    epoch = time.time()
    order = len(current_manifest['versions']) + 1
    id = VersionId(mode, code, epoch, order)
    compile_version(Version(id, changes, deletions), source, backup)
    return True

def create_version(source:str, backup:str, is_full:bool = False) -> bool:
    current_status = get_status_from_path(source)
    current_manifest = get_manifest(backup)
    deletions = []
    mode = VERSION_MODE_FULL if is_full else VERSION_MODE_PART
    order = len(current_manifest['versions']) + 1
    if not is_full:
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