#import os
#from backupbot.tools.directory import get_files
#from backupbot.tools.cryptography import get_file_hash
#from backupbot.tools.compression import extract_to_folder, update

from src.chelydra.core import create_full_version, create_partial_version

#update('project.zip', 'testarazo/prr.txt', 'main.py')
#extract_to_folder('project.zip', 'testarazo/prr.txt', 'output')
#
#print([get_file_hash(i) for i in get_files('.')])


print(create_partial_version('./playground/source', './playground/backup'))