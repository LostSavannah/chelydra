import time
from src.chelydra.backup import create_version, restore_into

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