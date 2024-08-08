import json
import os
from helpers import loadJson, dumpJson

class Hasher:
    def __init__(self):
        self.sizeMin = int(input("Minimum size to hash? (in bytes):"))
        self.inDir   = input("Folder to hash:")
        self.outDir  = input("Folder to save results:")
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
        self.recurse(self.inDir)
    
    def recurse(self, itemPath):
        for item in os.listdir(itemPath):
            jsonObj = {}
            itemPath = os.path.join(itemPath, item)
            
            if os.path.isfile(itemPath) and os.path.getsize(itemPath)>=self.sizeMin:
                fileHash = self.hash(itemPath)

                jsonObj["fileName"] = itemPath
                jsonObj["fileHash"] = fileHash

                self.jsonData.append(jsonObj)
                        
            elif os.path.isdir(itemPath):
                self.recurse(itemPath)
    def writeHashes(self):
        jsonDump(self.jsonData, f"{self.outDir}/hashes.json")



