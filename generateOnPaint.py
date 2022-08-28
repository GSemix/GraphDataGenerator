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
radius = 6.4

housing = input("[housing] >> ")
floor = input("[floor] >> ")

class VertexElem:
    def __init__(self, id, x, y):
        self.name = convertIdToName(id)
        self.housing = housing
        self.floor = floor
        self.neighbors = []
        self.x = str(round(float(x), 1))
        self.y = str(round(float(y), 1))
        
class EdgeElem:
    def __init__(self, x1, y1, x2, y2, vertex):
        self.x1 = str(round(float(x1), 1))
        self.y1 = str(round(float(y1), 1))
        self.x2 = str(round(float(x2), 1))
        self.y2 = str(round(float(y2), 1))
        self.vertex = getNameOnCoordinates(vertex, x1, y1, x2, y2)
        
def getNameOnCoordinates(vertex, x1, y1, x2, y2):
    global countErrors
    content1 = []
    content2 = []
    content = []

    for a in vertex:
        if ((float(a.x) - radius) <= float(x1) <= (float(a.x) + radius)) and ((float(a.y) - radius) <= float(y1) <= (float(a.y) + radius)):
            content1.append(a.name)
            
    for b in vertex:
        if ((float(b.x) - radius) <= float(x2) <= (float(b.x) + radius)) and ((float(b.y) - radius) <= float(y2) <= (float(b.y) + radius)):
            content2.append(b.name)
       
    if content1 == [] and content2 == []:
        print("\t[-] >> Error with appending EDGE with coordinates\t->   x1: {}, y1: {}, x2: {}, y2: {}    <-".format(x1, y1, x2, y2))
        countErrors += 1
    elif content1 == []:
        print("\t[-] >> Error with appending EDGE with coordinates\t->   x1: {}, y1: {}    <-\t2-nd VERTEX is {}".format(x1, y1, content2))
        countErrors += 1
    elif content2 == []:
        print("\t[-] >> Error with appending EDGE with coordinates\t->   x2: {}, y2: {}    <-\t1-st VERTEX is {}".format(x2, y2, content1))
        countErrors += 1
    elif content1 == content2 and len(content1) == 1:
        print("\t[-] >> Missing 2-nd VERTEX! Error with appending EDGE with coordinates\t->   x2: {}, y2: {}    <-\t1-st VERTEX is {}".format(x2, y2, content1))
        countErrors += 1
    else:
        content = list(set(content1 + content2))
            
    return content
        
def convertIdToName(id):
    if isinstance(id, str) and id != '':
        return id[1:]
        
    print("[-] >> Error in convertIdToName")

    return ''

def getPermitedHexSymbols():
    with open(nameFilePermittedHexSymbols, 'r') as file:
        return load(file)
        
def isValidId(id):
    if id == '' or id[0] != '#':
        return False

    return True
        
def getContentSVG(fileName, isSetRadius):
    global countErrors
    global radius
    file = minidom.parse(fileName)
    vertexList = []
    edgeList = []
    countCircles = 0
    countLines = 0
    countValideCircles = 0
    countValideLines = 0
    
    for path in file.getElementsByTagName('circle'):
        countCircles += 1
        unhexedId = clearId(path.getAttribute('id'))
    
        if isValidId(unhexedId):
            countValideCircles += 1
        
            if unhexedId[:5] != '#edge':
                if isSetRadius:
                    radius = float(path.getAttribute('r'))
                    isSetRadius = False
                        
                vertexList.append(VertexElem(unhexedId, path.getAttribute('cx'), path.getAttribute('cy')))
        else:
            countErrors += 1
            print("\t[-] >> Error with CIRCLE [id]\t->  {}  <-".format(unhexedId))
            
    for path in file.getElementsByTagName('circle'):
        unhexedId = clearId(path.getAttribute('id'))
    
        if isValidId(unhexedId) and unhexedId[:5] == '#edge':
            edgeList.append(EdgeElem(path.getAttribute('cx'), path.getAttribute('cy'), path.getAttribute('cx'), path.getAttribute('cy'), vertexList))
            
    for path in file.getElementsByTagName('line'):
        countLines += 1
        unhexedId = clearId(path.getAttribute('id'))
    
        if isValidId(unhexedId) and unhexedId[:5] == '#edge':
            edgeList.append(EdgeElem(path.getAttribute('x1'), path.getAttribute('y1'), path.getAttribute('x2'), path.getAttribute('y2'), vertexList))
            
            if len(edgeList[-1].vertex) < 2:
                edgeList.remove(edgeList[-1])
            else:
                countValideLines += 1
        else:
            countErrors += 1
            print("\t[-] >> Error with LINE [id]\t->  {}  <-".format(unhexedId))

    file.unlink()

    print("\n$$$$$\n$$$$$\t[+] >> set Radius = {}\n$$$$$\n$$$$$\t[?] >> Detected {} valid of {} CIRCLES\n$$$$$\t[?] >> Detected {} valid of {} LINES\n$$$$$".format(radius, countValideCircles, countCircles, countValideLines, countLines))
    
    return (vertexList, edgeList)
    
def isStringFloat(text):
    if text != '':
        if text[-1] == '.' or text[0] == '.':
            return False
        else:
            return text.replace('.', '', 1).isdigit()
            
    return False
    
def clearId(id):
    global countWarnings

    if isinstance(id, str) and id != '':
        for a in fromHex.keys():
            id = id.replace(a, fromHex[a])
        
        for a in getHexSymbols().keys():
            if a in id:
                countWarnings += 1
                print("#\n#\t[!] >> Be careful! Hex detected with [id] ->  {}  <-\n#".format(id))
                
                return id
            
        return id

    return ''
    
def checkRadius(arg):
    global radius

    if isStringFloat(arg):
        radius = round(float(arg), 1)
    
        return False

    print("\n$$$$$\n$$$$$\t[!] >> Radius is incorrect!", end = '')

    return True
    
def isStringFloat(text):
    if text != '':
        if text[-1] == '.' or text[0] == '.':
            return False
        else:
            return text.replace('.', '', 1).isdigit()
            
    return False
    
def getOneVertexJSON(name, housing, floor, x, y):
    return {
            "housing": housing,
            "floor": floor,
            "x": x,
            "y": y
            }
    
def getAllVertexJSON(vertex):
    content = {}
    
    for a in vertex:
        content['{}'.format(a.name)] = getOneVertexJSON(a.name, a.housing, a.floor, a.x, a.y)
    
    print("[+] >> Successfuly added {} vertex".format(len(content.keys())))
          
    return content
          
def writeVertexJSON(content):
    with open(nameFileVertex, 'w', encoding = 'utf-8') as file:
        file.write(dumps(content, sort_keys = False, indent = 4, ensure_ascii = False) + '\n')
        print("[+] >> Vertex saved in {}".format(nameFileVertex))
        
def getAllEdgeJSON(vertex, edges):
    content = {}
    clearedContent = {}
    count = 0
    
    for a in vertex:
        content['{}'.format(a.name)] = []
        
    for b in edges:
        for c in b.vertex:
            for d in b.vertex:
                if c != d and (d not in content['{}'.format(c)]):
                    content['{}'.format(c)].append(d)
        
    for e in content.keys():
        if content[e] != []:
            clearedContent[e] = content[e]
            
    for f in clearedContent.keys():
        for g in clearedContent[f]:
            count += 1
    
    print("[+] >> Successfuly added {} edges".format(count))
          
    return clearedContent
          
def writeEdgeJSON(content):
    with open(nameFileEdges, 'w', encoding = 'utf-8') as file:
        file.write(dumps(content, sort_keys = False, indent = 4, ensure_ascii = False) + '\n')
        print("[+] >> Edges saved in {}".format(nameFileEdges))
        
def getHexSymbols():
    with open(nameFileHexSymbols, 'r') as file:
        return load(file)

if __name__ == '__main__':
    nameFileSVG = argv[1]
    
    try:
        isSetRadius = checkRadius(argv[2])
    except IndexError:
        isSetRadius = True
        
    if isSetRadius:
        print("\n$$$$$")
        print("$$$$$\tThe radius will be copied from the 1-st VERTEX with a valid [id]\n$$$$$")
    
    fromHex = getPermitedHexSymbols()
    
    print("\n### Analyse ###\n")
    vertex, edges = getContentSVG(nameFileSVG, isSetRadius)
    
    print("\n### Information ###\n")
    
    vertexJson = getAllVertexJSON(vertex)
    writeVertexJSON(vertexJson)
    
    edgesJson = getAllEdgeJSON(vertex, edges)
    writeEdgeJSON(edgesJson)
    
    print("\n# End with {} Errors and {} Warning\n".format(countErrors, countWarnings))
    
    
