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

housing = input("\n[housing] >> ")
floor = input("[floor] >> ")

class VertexElem:
    def __init__(self, id, x, y):
        self.name = convertIdToName(id)
        self.housing = housing
        self.floor = floor
        self.x = str(round(float(x), 1))
        self.y = str(round(float(y), 1))
        self.x0 = None
        self.y0 = None
        
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
        print("\t[-] >> Error with appending EDGE<LINE> with coordinates\t->   x1: {}, y1: {}    <-\t2-nd VERTEX is {}".format(x1, y1, content2))
        countErrors += 1
    elif content2 == []:
        print("\t[-] >> Error with appending EDGE<LINE> with coordinates\t->   x2: {}, y2: {}    <-\t1-st VERTEX is {}".format(x2, y2, content1))
        countErrors += 1
    elif content1 == content2 and len(content1) == 1:
        print("\t[-] >> Missing 2-nd VERTEX! Error with appending EDGE<CIRCLE> with coordinates\t->   x2: {}, y2: {}    <-\t1-st VERTEX is {}".format(x2, y2, content1))
        countErrors += 1
    else:
        content = list(set(content1 + content2))
            
    return content
        
def convertIdToName(id):
    if isinstance(id, str) and id != '':
        return id.replace('#', '', 1)
        
    print("[-] >> Error in convertIdToName")

    return ''

def getPermitedHexSymbols():
    with open(nameFilePermittedHexSymbols, 'r') as file:
        return load(file)
        
def isValidId(id):
    if id == '' or id[0] != '#':
        return False

    return True
    
def isTwinInVertex(name, vertexList):
    for a in vertexList:
        if a.name == name:
            return True
            
    return False
        
def getContentSVG(fileName, isSetRadius):
    global countErrors
    global countWarnings
    global radius
    file = minidom.parse(fileName)
    vertexList = []
    edgeList = []
    countValideVertexCircles = 0
    countValideEdgeLines = 0
    countValideEdgeCircles = 0
    countValideZeroCircles = 0
    
    for path in file.getElementsByTagName('circle'):
        unhexedId = clearId(path.getAttribute('id'))
        
        for a in getHexSymbols().keys():
            if a in unhexedId:
                countWarnings += 1
                print("#\n#\t[!] >> Be careful! HEX detected with [id] ->  {}  <-\n#".format(unhexedId))
    
        if isValidId(unhexedId):
            if unhexedId[:5] != '#edge' and unhexedId[:3] != '#0#':
                if unhexedId[-1] == '_':
                    print("#\n#\t[!] >> Be careful! May be TWIN detected with [id] ->  {}  <-\n#".format(unhexedId))
                    countWarnings += 1

                if isSetRadius:
                    radius = float(path.getAttribute('r'))
                    isSetRadius = False
                    
                for a in unhexedId.split('#')[1:]:
                    if isTwinInVertex(a, vertexList) == False:
                        vertexList.append(VertexElem(a, path.getAttribute('cx'), path.getAttribute('cy')))
                        
                        if vertexList[-1].name == '':
                            vertexList.remove(vertexList[-1])
                        else:
                            countValideVertexCircles += 1
                    else:
                         print("\t[-] >> Error! Detected Twin CIRCLE [id]\t->  {}  <-".format(unhexedId))
        else:
            countErrors += 1
            print("\t[-] >> Error with CIRCLE [id]\t->  {}  <-".format(unhexedId))
            
    for path in file.getElementsByTagName('circle'):
        unhexedId = clearId(path.getAttribute('id'))
            
        if isValidId(unhexedId) and unhexedId[:3] == '#0#':
            
            for a in vertexList:
                if a.name == unhexedId[3:]:
                    if a.x0 == None and a.y0 == None:
                        a.x0 = path.getAttribute('cx')
                        a.y0 = path.getAttribute('cy')
                    else:
                        print("\t[-] >> Error! ZeroVertex already recorded [id]\t->  {}  <-".format(unhexedId[3:]))
                        countErrors += 1
                        
                    countValideZeroCircles += 1
                    break
                    
                if a == vertexList[-1]:
                    print("\t[-] >> Error! Vertex not found with ZeroVertex [id]\t->  {}  <-".format(unhexedId[3:]))
                    countErrors += 1
        
    for path in file.getElementsByTagName('circle'):
        unhexedId = clearId(path.getAttribute('id'))
    
        if isValidId(unhexedId) and unhexedId[:5] == '#edge':
            edgeList.append(EdgeElem(path.getAttribute('cx'), path.getAttribute('cy'), path.getAttribute('cx'), path.getAttribute('cy'), vertexList))
            
            if len(edgeList[-1].vertex) < 2:
                edgeList.remove(edgeList[-1])
            else:
                countValideEdgeCircles += 1
            
    for path in file.getElementsByTagName('line'):
        unhexedId = clearId(path.getAttribute('id'))
        
        for a in getHexSymbols().keys():
            if a in unhexedId:
                countWarnings += 1
                print("#\n#\t[!] >> Be careful! HEX detected with [id] ->  {}  <-\n#".format(unhexedId))
    
        if isValidId(unhexedId) and unhexedId[:5] == '#edge':
            edgeList.append(EdgeElem(path.getAttribute('x1'), path.getAttribute('y1'), path.getAttribute('x2'), path.getAttribute('y2'), vertexList))
            
            if len(edgeList[-1].vertex) < 2:
                edgeList.remove(edgeList[-1])
            else:
                countValideEdgeLines += 1
        else:
            countErrors += 1
            print("\t[-] >> Error with LINE [id]\t->  {}  <-".format(unhexedId))

    file.unlink()
    
    print()
    
    for a in vertexList:
        if a.x0 == None or a.y0 == None:
            print("[?] >> Missing ZeroVertex with [id]\t->  {}  <-".format(a.name))
            countWarnings += 1

    print("\n$$$$$\n$$$$$\t[+] >> set Radius = {}\n$$$$$\n$$$$$\t[+] >> Detected {} valid VERTEX<CIRCLE>\n$$$$$\t[+] >> Detected {} valid EDGE<LINE>\n$$$$$\t[+] >> Detected {} valid EDGE<CIRCLE>\n$$$$$\t[+] >> Detected {} valid ZeroVertex\n$$$$$".format(radius, countValideVertexCircles, countValideEdgeLines, countValideEdgeCircles, countValideZeroCircles))
    
    return (vertexList, edgeList)
    
def isStringFloat(text):
    if text != '':
        if text[-1] == '.' or text[0] == '.':
            return False
        else:
            return text.replace('.', '', 1).isdigit()
            
    return False
    
def clearId(id):
    if isinstance(id, str) and id != '':
        for a in fromHex.keys():
            id = id.replace(a, fromHex[a])
            
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
    
def getOneVertexJSON(name, housing, floor, x, y, x0, y0):
    if x0 == None or y0 == None:
        x0 = x
        y0 = y

    return {
            "housing": housing,
            "floor": floor,
            "x": x,
            "y": y,
            "x0": x0,
            "y0": y0
            }
    
def getAllVertexJSON(vertex):
    content = {}
    
    for a in vertex:
        content['{}'.format(a.name)] = getOneVertexJSON(a.name, a.housing, a.floor, a.x, a.y, a.x0, a.y0)
    
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
    
    
