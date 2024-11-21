import json
import os
from math import inf
import hashlib
from base64 import b64encode
from helpers import loadJson, dumpJson

#/home/kali/openipc-firmware/firmware_mod/v2

class Hasher:
    def __init__(self):
        self.sizeMin = int(input("Minimum size to hash? (in bytes): "))
        self.sizeMax = input("Maximum? (leave blank for None): ")
        if self.sizeMax == "": self.sizeMax = inf
        else: self.sizeMax = int(self.sizeMax)
        self.inDir   = input("Folder to hash: ")
        self.outDir  = input("Folder to save results: ")
        self.jsonData= []
    
    def hash(self, filePath):
        BLOCK_SIZE = 65536
        fileHash = hashlib.sha256()
        
        with open(filePath, 'rb') as file:
            fileBytes = file.read(BLOCK_SIZE)
            while len(fileBytes) > 0:
                fileHash.update(fileBytes)
                fileBytes = file.read(BLOCK_SIZE)

        return fileHash.hexdigest()

    def getHashes(self):
        self.recurse(self.inDir, 0)
    
    def recurse(self, itemPath, level):
        for item in os.listdir(itemPath):
            jsonObj = {}
            newPath = os.path.join(itemPath, item)
            itemExtension = item.split(".")[-1]
            if itemExtension == item: itemExtension = None

            numBytes = os.path.getsize(newPath)
            mTime = os.path.getmtime(newPath)

            if os.path.isfile(newPath) and numBytes >= self.sizeMin and numBytes <= self.sizeMax:
                fileHash = self.hash(newPath)
               
                jsonObj["key_hash"] = fileHash
                jsonObj["recursion_level"] = level
                jsonObj["bytes"] = numBytes
                jsonObj["mtime"] = mTime

                jsonObj["path"] = itemPath
                jsonObj["path_base64"] = str(b64encode(newPath.encode("ascii")))
                jsonObj["path_coding"] = "ascii"
                
                jsonObj["name"] = item
                jsonObj["name_base64"] = str(b64encode(item.encode("ascii")))
                jsonObj["name_coding"] = "ascii"
                
                jsonObj["extension"] = itemExtension
                jsonObj["extension_base64"] = str(b64encode(itemExtension.encode("ascii"))) if itemExtension else None
                jsonObj["extension_coding"] = "ascii" if itemExtension else None
                
                self.jsonData.append(jsonObj)
                        
            elif os.path.isdir(newPath):
                self.recurse(newPath, level + 1)
    def writeHashes(self):
        dumpJson(self.jsonData, f"{self.outDir}/hashes.json")



