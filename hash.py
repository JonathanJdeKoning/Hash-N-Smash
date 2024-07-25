import os
import hashlib
from functools import cache

class Hasher:
    def __init__(self, sizeMin, inDir, outDir):
        self.sizeMin = sizeMin
        self.inDir = inDir
        self.outDir = outDir
    
    @cache
    def getHash(self, filePath):
        BLOCK_SIZE = 65536
        fileHash = hashlib.sha256()
        
        with open(filePath, 'rb') as file:
            fileBytes = file.read(BLOCK_SIZE)
            while len(fileBytes) > 0: 
                fileHash.update(fileBytes)
                fileBytes = file.read(BLOCK_SIZE)

        return fileHash.hexdigest()

    def writeHashes(self, inDir, writeFile):
        for item in os.listdir(inDir):
            itemPath = os.path.join(inDir, item)
            
            if os.path.isfile(itemPath):
                fileHash = self.getHash(itemPath)
                writeFile.write(f"{itemPath}: {fileHash}\n")
            
            elif os.path.isdir(itemPath):
                self.writeHashes(itemPath, writeFile)

    def hashFolder(self):
        with open(self.outDir+"/hashes.txt", 'w') as writeFile:
            self.writeHashes(self.inDir, writeFile)

        

if __name__ == "__main__":
    sizeMin = int(input("Minimum size to hash (KB):"))
    inDir = input("Folder to hash:")
    outDir = input("Folder to save results:")

    myHasher = Hasher(sizeMin, inDir, outDir)

    myHasher.hashFolder()
    

