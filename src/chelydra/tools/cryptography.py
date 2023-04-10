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