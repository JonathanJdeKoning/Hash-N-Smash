import json
from base64 import b64encode

def loadJson(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)

def dumpJson(jsonData, filePath):
    with open(filePath, "w") as file:
        json.dump(jsonData, file, indent=4)

def b64(s: str) -> str:
    if not s: return None
    return str(b64encode(s.encode("ascii")))

def extension(s: str) -> str:
    if s[0] == ".":
        return None
    if "." not in s:
        return None
    return s.split(".")[-1]

def print_header(s: str) -> None:
    N = len(s)
    print(f"{'-'*(N+2)}")
    print(f"|{s}|")
    print(f"{'-'*(N+2)}")
