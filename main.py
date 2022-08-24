#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv
from json import dumps
from xml.dom import minidom

nameFileVertex = "Vertex.json"
nameFileEdges = "Edges.json"
fromHex = {
    '_x7C_': '|',
    '_x26_': '&'
}

housing = input("[housing] >> ")
floor = input("[floor] >> ")

class Elem:
    def __init__(self, id, x, y):
        id = clearId(id)
        
        self.name = convertIdToName(id)
        self.housing = housing
        self.floor = floor
        self.neighbors = convertIdToNeighboor(id)
        self.x = str(round(float(x), 1))
        self.y = str(round(float(y), 1))
        
def clearId(id):
    if isinstance(id, str) and id != '':
        if id[0] == '_':
            id = id[1:]
            
        for a in fromHex.keys():
            id = id.replace(a, fromHex[a])
            
        return id
        
    return ''

def convertIdToName(id):
    if isinstance(id, str) and id != '':
        return id.split('_')[0]
        
    return ''

def convertIdToNeighboor(id):
    if isinstance(id, str) and id != '' and len(id.split('_')) >= 2:
        return [neighbor for neighbor in id.split('_')[1:] if neighbor != '']
            
    return []

def clearContent(content):
    filteredContent = list(filter(lambda elem: elem.name != '' and elem.neighbors != [], content))
    
    for elem in content:
        if elem not in filteredContent:
            print("\t[-] >> Error with [name]\t->  {}  <-".format(elem.name))

    return filteredContent

def getContentSVG(fileName):
    file = minidom.parse(fileName)
    content = [Elem(path.getAttribute('id'), path.getAttribute('cx'), path.getAttribute('cy')) for path in file.getElementsByTagName('circle') if path.getAttribute('id') != '']
    file.unlink()
    
    return clearContent(content)

def getOneVertexJSON(name, housing, floor, x, y):
    return {
            "housing": housing,
            "floor": floor,
            "x": x,
            "y": y
            }
    
def getAllVertexJSON(contentSVG):
    content = {}
    
    for a in contentSVG:
        content['{}'.format(a.name)] = getOneVertexJSON(a.name, a.housing, a.floor, a.x, a.y)
    
    print("[+] >> Successfuly added {} vertex".format(len(content.keys())))
          
    return content
          
def writeVertexJSON(content):
    with open(nameFileVertex, 'w', encoding= 'utf-8') as file:
        file.write(dumps(content, sort_keys = False, indent = 4, ensure_ascii = False) + '\n')
        print("[+] >> Vertex saved in {}".format(nameFileVertex))
    
def getAllEdgeJSON(contentSVG):
    content = {}
    
    for a in contentSVG:
        content['{}'.format(a.name)] = a.neighbors
    
    print("[+] >> Successfuly added {} edges".format(len(content.keys())))
          
    return content
          
def writeEdgeJSON(content):
    with open(nameFileEdges, 'w', encoding= 'utf-8') as file:
        file.write(dumps(content, sort_keys = False, indent = 4, ensure_ascii = False) + '\n')
        print("[+] >> Edges saved in {}".format(nameFileEdges))
          
if __name__ == '__main__':
    nameFileSVG = argv[1]
    contentSVG = getContentSVG(nameFileSVG)
    
    content = getAllVertexJSON(contentSVG)
    writeVertexJSON(content)
    
    content = getAllEdgeJSON(contentSVG)
    writeEdgeJSON(content)
