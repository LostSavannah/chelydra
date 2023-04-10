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