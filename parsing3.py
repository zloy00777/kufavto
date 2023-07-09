#!/usr/bin/python3
import glob
import json

arrIds = []
global jsonStr
def writeIdsFile():
    for file in glob.glob('./*.txt'):
        arrIds.append(file.replace('.txt', '').replace('.\\', ''))
    jsonStr = json.dumps(arrIds)
    with open("ids.json", 'w') as f:
        f.write(jsonStr)
def addIdFile(id):
    ids = readIdsFile()
    ids.append(id)
    jsonStr = json.dumps(ids)
    with open("ids.json", 'w') as f:
        f.write(jsonStr)
def readIdsFile():
    with open('ids.json', 'r') as fcc_file:
        fcc_data = json.load(fcc_file)
    return fcc_data
def findIdFile(id):
    file = readIdsFile()
    if id in file:
        return 0
    else:
        return 1

file = readIdsFile()
print(len(file))
print(file)
#addIdFile(116412210)
print(findIdFile(116412210))
print(findIdFile(116412211))