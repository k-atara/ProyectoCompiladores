from os import pipe
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import sys
import re

listaTokens=[]
listaCategoria=['MULTICOM','DX','COMMENT','LPAR','RPAR','LSQB','RSQB','LBRACE','RBRACE','SEMI','COMMA','MINUS','PLUS','STAR','SLASH','PERCENT','EQEQUAL','EQUAL','NOTEQUAL','GREATEREQUAL','LESSEQUAL','LESS','GREATER','MAIN','PRINTS','AND','BREAK','DEC','DO','ELIF','ELSE','FALSE','IF','INC','NOT','OR','RETURN','TRUE','VAR','WHILE','IDENTIFIER','INTEGER','STRING','CHARACTER','DX2','ENTER','TAB','READLINE','SPACE','RDOUBLESLASH','CSIMPLE','CDOUBLE','ILEGAL']
row = 1
column=0

class Token:
    def __init__(self, lexema,category,row,column):
        self.lexema=lexema
        self.category=category
        self.row=row
        self.column=column

def IterarGrupos(m):
    global row
    global column

    grupo=m.groups()
    for i in range(len(grupo)):
        if(grupo[i]!=None):
            if(listaCategoria[i]=='ENTER'):
                row+=1
                break
            elif(listaCategoria[i]=='MULTICOM'):
                x=grupo[i]
                num=x.count('\n')
                row+=num         
                break
            elif(listaCategoria[i]=='SPACE' or listaCategoria[i]=='TAB' or listaCategoria[i]=='COMMENT'):
                break
            elif(listaCategoria[i]=='ILEGAL'):
                print("ERROR EN LA LINEA "+ str(row))
                sys.exit()
            else:
                token = Token(grupo[i],listaCategoria[i],row,column)
                listaTokens.append(token)
                break


#Lista del nombre de los simbolos o palabras
#lCat=['']

nom_archivo = sys.argv[1]

file=open(nom_archivo)
code=file.read()
file.close()

##########################################################################################################
##########################################################################################################

#regexFinal=r'([\(][\*](.|\n)*?[\*][\)])'
regexFinal=r'([(][*](.|\n)*?[*][)])|([-]{2}.*)|([(])|([)])|([[])|([]])|([{])|([}])|([;])|([,])|([-])|([+])|([*])|([/])|([%])|([==])|([=])|([<>])|([>=])|([<=])|([<])|([>])|(main\b)|(prints\b)|(and\b)|(break\b)|(dec\b)|(do\b)|(elif\b)|(else\b)|(false\b)|(if\b)|(inc\b)|(not\b)|(or\b)|(return\b)|(true\b)|(var\b)|(while\b)|([a-zA-Z][a-zA-Z0-9_]*)|(\d+)|(\".*\")|(\'([^\n\'\\]|\\[nrt\\\'"])\'|\'.\')|(\n)|(    )|(\r)|(\s)|(\\)|(\')|(\")|(.)'


#falta unicode y |('(\\[u][[0-9a-fA-F]{6})'|'([^\n'\\]|\\[nrt\\'"])'|'.')|("([^\n'\\]|.*)")

#('(\\[u][[0-9a-fA-F]{6})'|'([^\n'\\]|\\[nrt\\'"])'|'.')|("([^\n'\\]|.*)")
#regexFinal=r'([(][*](.|\n)*?[*][)])|(([-]{2}.*))|(\n)|(\s)|(\r)|(\t)|(\\)|(\')|(\")|([(])|([)])|([[])|([]])|([{])|([}])|([;])|([,])|([-])|([+])|([*])|([/])|([%])|([==])|([=])|([<>])|([>=])|([<=])|([<])|([>])|(and\b)|(break\b)|(dec\b)|(do\b)|(elif\b)|(else\b)|(false\b)|(if\b)|(inc\b)|(not\b)|(or\b)|(return\b)|(true\b)|(var\b)|(while\b)|([a-zA-Z][a-zA-Z0-9_]*)|(\d+)|(.)'



respuestaRegex=re.finditer(regexFinal,code)
nToken=0



for m in respuestaRegex: 
    nToken+=1
    print(str(nToken)+'\n')
    print(m.groups(),m.start(),m.end())
    print("-----------------")
    print('\n')
    IterarGrupos(m)

for j in range(len(listaTokens)):
    print(listaTokens[j].lexema)
print("Numero de tokens: " +str(len(listaTokens)))
print("Numero de filas: "+str(row))







