#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from xml.dom import minidom

nameFileVertex = "Vertex.json"
housing = input("[housing] >> ")
floor = input("[floor] >> ")

class Elem:
    def __init__(self, name, x, y):
        self.name = convertIdToString(name)
        self.housing = housing
        self.floor = floor
        self.x = str(round(float(x), 1))
        self.y = str(round(float(y), 1))

def convertIdToString(id):
    if isinstance(id, str) and id != '':
        if id[0] == '_':
            return id[1:]
        else:
            return id
    else:
        return ''

def clearContent(content):
    for elem in content:
        if elem.name == '':
            content.remove(elem)
    
    return content

def getContentSVG(fileName):
    file = minidom.parse(fileName)
    content = [Elem(path.getAttribute('id'), path.getAttribute('cx'), path.getAttribute('cy')) for path in file.getElementsByTagName('circle') if path.getAttribute('id') != '']
    file.unlink()
    
    return clearContent(content)

def getJSON(name, housing, floor, x, y):
    return {
        "housing": str(housing),
            "floor": str(floor),
            "x": str(x),
            "y": str(y)
            }
    
def getContentJSON(contentSVG):
    content = {}
    
    for a in contentSVG:
        content['{}'.format(a.name)] = getJSON(a.name, a.housing, a.floor, a.x, a.y)
    
    print("[+] >> Successfuly added {} elems".format(len(content.keys())))
          
    return content
          
def writeJSON(content):
    with open(nameFileVertex, 'w', encoding= 'utf-8') as file:
        file.write(json.dumps(content, sort_keys = False, indent = 4, ensure_ascii = False) + '\n')
        print("[+] >> Vertex saved in {}".format(nameFileVertex))
          
if __name__ == '__main__':
    nameFileSVG = sys.argv[1]
    content = getContentJSON(getContentSVG(sys.argv[1]))
    writeJSON(content)
