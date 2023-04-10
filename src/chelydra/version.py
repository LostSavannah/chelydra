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