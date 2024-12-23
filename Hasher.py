import json
import os
from math import inf
import hashlib
from helpers import loadJson, dumpJson, b64, extension
from datatypes import FileData
from dataclasses import asdict

#C:/Users/jj720/IOT/firmware

class Hasher:
    def __init__(self, size_min, size_max, in_dir, out_dir):
        self.json_data = []

        self.size_min = size_min
        self.size_max = size_max
        self.in_dir = in_dir
        self.out_dir = out_dir
    
    def hash(self, file_path):
        BLOCK_SIZE = 65536
        file_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as file:
            file_bytes = file.read(BLOCK_SIZE)
            while len(file_bytes) > 0:
                file_hash.update(file_bytes)
                file_bytes = file.read(BLOCK_SIZE)

        return file_hash.hexdigest()

    def getHashes(self):
        self.recurse(self.in_dir, 0)
    
    def recurse(self, item_path, level):
        for item in os.listdir(item_path):
            new_path = os.path.join(item_path, item)
            item_extension = extension(item)
            num_bytes = os.path.getsize(new_path)
            mTime = os.path.getmtime(new_path)
            if os.path.isfile(new_path) and num_bytes >= self.size_min and num_bytes <= self.size_max:
                file_hash = self.hash(new_path)
                file = FileData(
                    name=item,
                    name_base64=b64(item),
                    name_coding="ascii",
                    path=item_path,
                    path_base64=b64(item_path),
                    path_coding="ascii",
                    extension=item_extension,
                    extension_base64=b64(item_extension),
                    extension_coding="ascii",
                    key_hash=file_hash,
                    recursion_level=level,
                    bytes=num_bytes,
                    mtime=mTime,
                )
                
                self.json_data.append(asdict(file))
                        
            elif os.path.isdir(new_path):
                self.recurse(new_path, level + 1)

    def writeHashes(self):
        dumpJson(self.json_data, f"{self.out_dir}/metadata.json")



