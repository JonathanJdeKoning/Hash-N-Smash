import os
import json
import hashlib

class File:
    def __init__(self):
        pass

class Hasher:
    def __init__(self, sizeMin, inDir, outDir):
        self.sizeMin = sizeMin
        self.inDir = inDir
        self.outDir = outDir
        self.jsonData = []
    
    def getHash(self, filePath):
        BLOCK_SIZE = 65536
        fileHash = hashlib.sha256()
        
        with open(filePath, 'rb') as file:
            fileBytes = file.read(BLOCK_SIZE)
            while len(fileBytes) > 0:
                fileHash.update(fileBytes)
                fileBytes = file.read(BLOCK_SIZE)

        return fileHash.hexdigest()

    def writeHashes(self, inDir):
        for item in os.listdir(inDir):
            jsonObj = {}
            itemPath = os.path.join(inDir, item)
            
            if os.path.isfile(itemPath) and os.path.getsize(itemPath)>=self.sizeMin:
                fileHash = self.getHash(itemPath)

                jsonObj["fileName"] = itemPath
                jsonObj["fileHash"] = fileHash

                self.jsonData.append(jsonObj)
                           
            elif os.path.isdir(itemPath):
                self.writeHashes(itemPath)


if __name__ == "__main__":
    sizeMin = int(input("Minimum size to hash (bytes):"))
    inDir = input("Folder to hash:")
    outDir = input("Folder to save results:")

    myHasher = Hasher(sizeMin, inDir, outDir)

    myHasher.writeHashes(inDir)
    with open(f"{outDir}/hashes.json", "w") as file:
        json.dump(myHasher.jsonData, file, indent=4)
