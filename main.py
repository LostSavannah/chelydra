#import os
#from backupbot.tools.directory import get_files
#from backupbot.tools.cryptography import get_file_hash
#from backupbot.tools.compression import extract_to_folder, update

import time
from src.chelydra.core import create_version, restore_into

#update('project.zip', 'testarazo/prr.txt', 'main.py')
#extract_to_folder('project.zip', 'testarazo/prr.txt', 'output')
#
#print([get_file_hash(i) for i in get_files('.')])

source = r"D:\test\chelydra\source"
backup = r"D:\test\chelydra\backup"
restore = r"D:\test\chelydra\restore"

restore_into(backup, restore)
while True:
    if(create_version(source, backup)):
        print('Version created')
    else:
        print('No changes')
    time.sleep(10)