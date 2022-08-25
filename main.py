#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv
from json import dumps
from json import load
from xml.dom import minidom

nameFileVertex = "Vertex.json"
nameFileEdges = "Edges.json"
nameFileHexSymbols = "hexSymbols.json"
nameFilePermittedHexSymbols = "permittedHexSymbols.json"
fromHex = {}
countWarnings = 0
countErrors = 0

housing = input("[housing] >> ")
floor = input("[floor] >> ")

class Elem:
    def __init__(self, id, x, y):
        self.name = convertIdToName(id)
        self.housing = housing
        self.floor = floor
        self.neighbors = convertIdToNeighboor(id)
        self.x = str(round(float(x), 1))
        self.y = str(round(float(y), 1))
        
def getHexSymbols():
    with open(nameFileHexSymbols, 'r') as file:
        return load(file)
        
def clearId(id):
    global countWarnings

    if isinstance(id, str) and id != '':
        for a in fromHex.keys():
            id = id.replace(a, fromHex[a])
            
        hexSymbols = getHexSymbols()
        
        for a in hexSymbols.keys():
            if a in id:
                countWarnings += 1
                print("#\n#\t[!] >> Be careful! Hex detected with [id] ->  {}  <-\n#".format(id))
                
                return id
            
        return id

    return ''

def convertIdToName(id):
    if isinstance(id, str) and id != '':
        return id.split('_')[0][1:]
        
    print("[-] >> Error in convertIdToName")

    return ''

def convertIdToNeighboor(id):
    if isinstance(id, str) and id != '' and len(id.split('_')) >= 2:
        return [neighbor for neighbor in id.split('_')[1:] if neighbor != '']
        
    print("[-] >> Error in convertIdToNeighboor")
            
    return []

def getContentSVG(fileName):
    file = minidom.parse(fileName)
    content = []
    count = 0
    global countErrors
    
    for path in file.getElementsByTagName('circle'):
        unhexedId = clearId(path.getAttribute('id'))
    
        if isValidId(unhexedId):
            content.append(Elem(unhexedId, path.getAttribute('cx'), path.getAttribute('cy')))
        else:
            countErrors += 1
            print("\t[-] >> Error with [id]\t->  {}  <-".format(unhexedId))
            
        count += 1

    file.unlink()
    
    return (content, count)
    
def isValidId(id):
    if id == '' or id[0] != '#' or len(id.split('_')) == 1 or ('' in id.split('_')):
        return False

    return True

def getOneVertexJSON(name, housing, floor, x, y):
    return {
            "housing": housing,
            "floor": floor,
            "x": x,
            "y": y
            }
    
def getAllVertexJSON(contentSVG, count):
    content = {}
    
    for a in contentSVG:
        content['{}'.format(a.name)] = getOneVertexJSON(a.name, a.housing, a.floor, a.x, a.y)
    
    print("[+] >> Successfuly added {} of {} vertex".format(len(content.keys()), count))
          
    return content
          
def writeVertexJSON(content):
    with open(nameFileVertex, 'w', encoding = 'utf-8') as file:
        file.write(dumps(content, sort_keys = False, indent = 4, ensure_ascii = False) + '\n')
        print("[+] >> Vertex saved in {}".format(nameFileVertex))
    
def getAllEdgeJSON(contentSVG, count):
    content = {}
    
    for a in contentSVG:
        content['{}'.format(a.name)] = a.neighbors
    
    print("[+] >> Successfuly added {} of {} edges".format(len(content.keys()), count))
          
    return content
          
def writeEdgeJSON(content):
    with open(nameFileEdges, 'w', encoding = 'utf-8') as file:
        file.write(dumps(content, sort_keys = False, indent = 4, ensure_ascii = False) + '\n')
        print("[+] >> Edges saved in {}".format(nameFileEdges))
        
def getPermitedHexSymbols():
    with open(nameFilePermittedHexSymbols, 'r') as file:
        return load(file)
        
def Analyse(content):
    for a in content.keys():
        for b in content[a]:
            if b not in content.keys():
                print("[?] >> '{}' has unknown neighboor '{}'".format(a, b))
          
if __name__ == '__main__':
    fromHex = getPermitedHexSymbols()

    print("\n### Warnings and Errors ###\n")

    nameFileSVG = argv[1]
    contentSVG, count = getContentSVG(nameFileSVG)
    
    print("\n### Information ###\n")
    
    content = getAllVertexJSON(contentSVG, count)
    writeVertexJSON(content)
    
    content = getAllEdgeJSON(contentSVG, count)
    writeEdgeJSON(content)
    
    print("\n### Analyse ###\n")
    
    Analyse(content)
    
    print("\n# End with {} Errors and {} Warning\n".format(countErrors, countWarnings))
