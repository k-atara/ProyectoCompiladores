from os import pipe
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import sys
import re

class Token:
    def __init__(self, lexema,category,row,column):
        self.lexema=lexema
        self.category=category
        self.row=row
        self.column=column

#Lista del nombre de los simbolos o palabras
lCat=['']
listaTokens=[]

nom_archivo = sys.argv[1]

file=open(nom_archivo)
code=file.read()
file.close()

##########################################################################################################
##########################################################################################################
print(type(code))
print(code)

#falta unicode
regexFinal=r'''
([(][*](.|\n)*?[*][)])
|(([-]{2}.*))
|(\n)
|(\s)
|(\r)
|(\t)
|(\\)
|(\')
|(\")
|([(])
|([)])
|([[])
|([]])
|([{])
|([}])
|([;])
|([,])
|([-])
|([+])
|([*])
|([/])
|([%])
|([==])
|([=])
|([<>])
|([>=])
|([<=])
|([<])
|([>])
|(and\b)
|(break\b)
|(dec\b)
|(do\b)
|(elif\b)
|(else\b)
|(false\b)
|(if\b)
|(inc\b)
|(not\b)
|(or\b)
|(return\b)
|(true\b)
|(var\b)
|(while\b)
|([a-zA-Z][a-zA-Z0-9_]*)
|(\d+)
|('(\\[u][[0-9a-fA-F]{6})'|'([^\n'\\]|\\[nrt\\'"])'|'.')
|("([^\n'\\]|.*)")
|(.)
'''

respuestaRegex=re.finditer(regexFinal,code)
nToken=0
for m in respuestaRegex: 
    nToken+=1
    print(str(nToken)+'\n')
    print(m.groups(),m.start(),m.end())
    print("-----------------")
    print('\n')