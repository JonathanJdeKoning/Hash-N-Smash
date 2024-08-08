import json

def loadJson(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)

def dumpJson(jsonData, filePath):
    with open(filePath, "w") as file:
        json.dump(jsonData, file, indent=4)
