from typing import Any, Dict, List

VERSION_MODE_FULL = 'FULL'
VERSION_MODE_PART = 'PART'

class VersionId:
    def __init__(self, mode:str = None, code:str = None, epoch:float = None, order:int = None) -> None:
        self.mode = mode or VERSION_MODE_FULL
        self.code = code or ''
        self.epoch = epoch or 0.0
        self.order = order or 0
        if self.mode not in [VERSION_MODE_FULL, VERSION_MODE_PART]:
            raise Exception('Invalid mode')

class Version:
    def __init__(self, id:VersionId = None, changes:Dict[str, str] = None, deletions:List[str] = None) -> None:
        self.id = id or VersionId()
        self.changes = changes or {}
        self.deletions = deletions or []

    def is_full(self) -> bool:
        return self.id.mode == VERSION_MODE_FULL

    def load(self, d:Dict[str, Any]):
        self.id.mode = d['mode']
        self.id.code = d['code']
        self.id.epoch = d['epoch']
        self.id.order = d['order']
        self.changes = d['changes']
        self.deletions = d['deletions']
        return self

    def get_dict(self)->Dict[str, Any]:
        return {
            "mode": self.id.mode,
            "code": self.id.code,
            "epoch": self.id.epoch,
            "order": self.id.order,
            "changes": self.changes,
            "deletions": self.deletions
        }

    def get_filename(self, posfix:str = None):
        posfix = posfix or ''
        order = str(self.id.order).rjust(8, '0')
        mode = self.id.mode
        code = self.id.code
        return f'[{mode}][{order}][{code}]{posfix}'