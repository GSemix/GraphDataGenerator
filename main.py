#!/usr/bin/python3

import sys
from xml.dom import minidom

class Elem:
    def __init__(self, name, x, y):
        self.name = convertIdToString(name)
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
    
def getContentSVG(svgFileName):
    file = minidom.parse(svgFileName)
    content = [Elem(path.getAttribute('id'), path.getAttribute('cx'), path.getAttribute('cy')) for path in file.getElementsByTagName('circle') if path.getAttribute('id') != '']
    file.unlink()
    
    return clearContent(content)

if __name__ == '__main__':
    svgFileName = sys.argv[1]
    exampleJsonFileName = sys.argv[2]
    
    for x in getContentSVG(svgFileName):
        print(x.name, end = ' - ')
        print(x.x, end = ' - ')
        print(x.y, end = '\n')
