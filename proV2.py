from os import pipe
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from anytree import Node, RenderTree
import subprocess
import sys
import re
import copy

#-------------------------------------------------------------------------------TOKENIZADOR

listaTokens=[]
listaCategoria=['MULTICOM','DX','COMMENT','LPAR','RPAR','LSQB','RSQB','LBRACE','RBRACE','SEMI','COMMA','MINUS','PLUS','STAR','SLASH','PERCENT','EQEQUAL','NOTEQUAL','GREATEREQUAL','LESSEQUAL','LESS','EQUAL','GREATER','MAIN','PRINTS','AND','BREAK','DEC','DO','ELIF','ELSE','FALSE','IF','INC','NOT','OR','RETURN','TRUE','VAR','WHILE','IDENTIFIER','INTEGER','STRING','CHARACTER','CHARACTER','CHARACTER','ENTER','TAB','READLINE','SPACE','RDOUBLESLASH','CSIMPLE','CDOUBLE','ILEGAL']
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
            tokenLength= m.end()-m.start()
            if(listaCategoria[i]=='ENTER'):
                row+=1
                column=m.start()+tokenLength
                break
            elif(listaCategoria[i]=='MULTICOM'):
                x=grupo[i]
                num=x.count('\n')
                row+=num         
                break
            elif(listaCategoria[i]=='SPACE' or listaCategoria[i]=='TAB' or listaCategoria[i]=='COMMENT'):
                break
            elif(listaCategoria[i]=='ILEGAL'):
                print("ERROR EN LA LINEA "+ str(row) + " EN LA COLUMNA " + str(m.start()-column+1))
                sys.exit()
            else:
                columnToken=m.start()-column+1
                if(listaCategoria[i]=='MAIN' or listaCategoria[i]=='PRINTS'):
                    token = Token(grupo[i],'IDENTIFIER',row,columnToken)
                else:
                    token = Token(grupo[i],listaCategoria[i],row,columnToken)
                listaTokens.append(token)
                break

nom_archivo = sys.argv[1]

file=open(nom_archivo)
#file = open(r"path", "r")
code=file.read()
file.close()

##########################################################################################################
##########################################################################################################

#regexFinal=r'([\(][\*](.|\n)*?[\*][\)])'
regexFinal=r'([(][*](.|\n)*?[*][)])|([-]{2}.*)|([(])|([)])|([[])|([]])|([{])|([}])|([;])|([,])|([-])|([+])|([*])|([/])|([%])|(==)|(<>)|(>=)|(<=)|([<])|([=])|([>])|(main\b)|(prints\b)|(and\b)|(break\b)|(dec\b)|(do\b)|(elif\b)|(else\b)|(false\b)|(if\b)|(inc\b)|(not\b)|(or\b)|(return\b)|(true\b)|(var\b)|(while\b)|([a-zA-Z][a-zA-Z0-9_]*)|(\d+)|(\".*\")|(\'\\[u][0-9a-fA-F]{6}\')|(\'([^\n\'\\]|\\[nrt\\\'"])\'|\'.\')|(\n)|(    )|(\r)|(\s)|(\\)|(\')|(\")|(.)'

#falta unicode y |('(\\[u][[0-9a-fA-F]{6})'|'([^\n'\\]|\\[nrt\\'"])'|'.')|("([^\n'\\]|.*)")

respuestaRegex=re.finditer(regexFinal,code)
nToken=0

for m in respuestaRegex: 
    nToken+=1
    # print(str(nToken)+'\n')
    # print(m.groups(),m.start(),m.end())
    # print("-----------------")
    # print('\n')
    IterarGrupos(m)

for j in range(len(listaTokens)):
    print("Token numero: "+str(j+1) + ", Lexema: " + listaTokens[j].lexema + ", Categoria/Nombre: " + listaTokens[j].category + ", Row: "+ str(listaTokens[j].row) + ", Column: "+ str(listaTokens[j].column))

print("----------------------------------------------------")
print("Numero de tokens: " +str(len(listaTokens)))
print("Numero de filas: "+str(row))
print("----------------------------------------------------")

#---------------------------------------------------------------------------------------------PARSER
#GRAMÁTICA LIBRE DE CONTEXTO
# program -> deflist
# deflist -> deflist1
# deflist1 -> def deflist1
# deflist1 -> ''
# def -> vardef
# def -> fundef
# vardef -> var varlist ;
# varlist -> idlist
# idlist -> id idlistcont
# idlistcont -> , id idlistcont
# idlistcont -> ''
# fundef -> id ( paramlist ) { vardeflist stmtlist }
# paramlist -> idlist
# paramlist -> ''
# vardeflist -> vardeflist1
# vardeflist1 -> vardef vardeflist1
# vardeflist1 -> ''
# stmtlist -> stmtlist1
# stmtlist1 -> stmt stmtlist1
# stmtlist1 -> ''

# stmt -> id stmtP
# stmt -> stmtincr
# stmt -> stmtdecr
# stmt -> stmtif
# stmt -> stmtwhile
# stmt -> stmtdowhile
# stmt -> stmtbreak
# stmt -> stmtreturn
# stmt -> stmtempty

# stmtP -> = expr ; 
# stmtP -> ( exprlist ) ;
# stmtincr -> inc id ;
# stmtdecr -> dec id ;

# exprlist -> expr exprlistcont
# exprlist -> ''
# exprlistcont -> , expr exprlistcont
# exprlistcont -> ''

# stmtif -> if ( expr ) { stmtlist } elseiflist elsel
# elseiflist -> elseiflist1

# elseiflist1 -> elif ( expr ) { stmtlist } elseiflist1
# elseiflist1 -> ''
# elsel -> else { stmtlist }
# elsel -> ''
# stmtwhile -> while ( expr ) { stmtlist }
# stmtdowhile -> do { stmtlist } while ( expr ) ;
# stmtbreak -> break ;
# stmtreturn -> return expr ;
# stmtempty -> ;

# expr -> expror
# expror -> exprand expror1
# expror1 -> or exprand expror1
# expror1 -> '' 
# exprand -> exprcomp exprand1
# exprand1 -> and exprcomp exprand1
# exprand1 -> ''
# exprcomp -> exprrel exprcomp1
# exprcomp1 -> opcomp exprrel exprcomp1
# exprcomp1 -> ''

# opcomp -> ==
# opcomp -> <>
# exprrel -> expradd exprrel1
# exprrel1 -> oprel expradd exprrel1
# exprrel1 -> ''
# oprel -> <
# oprel -> <=
# oprel -> >
# oprel -> >=
# expradd -> exprmul expradd1
# expradd1 -> opadd exprmul expradd1
# expradd1 -> ''

# opadd -> +
# opadd -> −
# exprmul -> exprunary exprmul1
# exprmul1 -> opmul exprunary exprmul1
# exprmul1 -> ''
# opmul -> *
# opmul -> /
# opmul -> %
# exprunary -> opunary exprunary
# exprunary -> exprprimary
# opunary -> +
# opunary -> −
# opunary -> not

# exprprimary -> id exprprimaryP
# exprprimary -> array
# exprprimary -> lit
# exprprimary -> ( expr )

# exprprimaryP -> ''
# exprprimaryP -> ( exprlist ) 
# array -> [ exprlist ]
# lit -> litbool
# lit -> litint
# lit -> litchar
# lit -> litstr

pProgram = ['VAR', 'IDENTIFIER']
pDeflist = ['VAR', 'IDENTIFIER']
pDeflistP = ['VAR', 'IDENTIFIER']
pDef = ['VAR', 'ID']
pVardef = ['VAR']
pVarlist = ['IDENTIFIER']
pIdlist = ['IDENTIFIER']
pIdlistcont = ['COMMA']
pFundef = ['IDENTIFIER']
pParamlist = ['IDENTIFIER']
pVardeflist = ['VAR']
pVardeflistP = ['VAR']
pStmtlist = ['IDENTIFIER', 'INC', 'DEC', 'IF', 'WHILE', 'DO', 'BREAK', 'RETURN', 'SEMI']
pStmtlistP = ['IDENTIFIER', 'INC', 'DEC', 'IF', 'WHILE', 'DO', 'BREAK', 'RETURN', 'SEMI']
pStmt = ['IDENTIFIER', 'INC', 'DEC', 'IF', 'WHILE', 'DO', 'BREAK', 'RETURN', 'SEMI']
pStmtP = ['EQUAL', 'LPAR']
pStmtIncr = ['INC']
pStmtDecr = ['DEC']
pExprlist = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExprlistcont = ['COMMA']
pStmtif = ['IF']
pElseiflist = ['ELIF']
pElseiflistP = ['ELIF']
pElsel = ['ELSE']
pStmtwhile = ['WHILE']
pStmtdowhile = ['DO']
pStmtbreak = ['BREAK']
pStmtreturn = ['RETURN']
pStmtempty = ['SEMI']
pExpr = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExpror = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExprorP = ['OR']
pExprand = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExprandP = ['AND']
pExprcomp = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExprcompP = ['EQEQUAL', 'NOTEQUAL']
pOpcomp = ['EQEQUAL', 'NOTEQUAL']
pExprrel = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExprrelP = ['LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL']
pOprel = ['LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL']
pExpradd = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExpraddP = ['PLUS', 'MINUS']
pOpadd = ['PLUS', 'MINUS']
pExprmul = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExprmulP = ['STAR', 'SLASH', 'PERCENT']
pOpmul = ['STAR', 'SLASH', 'PERCENT']
pExprunary = ['PLUS', 'MINUS', 'NOT', 'IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pOpunary = ['PLUS', 'MINUS', 'NOT']
pExprprimary = ['IDENTIFIER', 'LPAR', 'LSQB', 'TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']
pExprprimaryP = ['LPAR']
pArray = ['LSQB']
pLit = ['TRUE', 'FALSE', 'INTEGER', 'CHARACTER', 'STRING']

contador=-1
lEntrada=len(listaTokens)
vEntrada = listaTokens

curToken = ""

#VARIABLES PARA TABLA DE SIMBOLOS

class TSimbolo:
    def __init__(self, declared, tokenType, name, dataType, size, params, ret, scope ):
        self.declared = declared #verificar si ya existia ese id o no (TRUE FALSE)
        self.tokenType = tokenType #tipo de token (id, funcion)
        self.name = name #nombre de token
        self.dataType = dataType #si es un id, verificar su literal 
        self.size = size #...
        self.params = params #para ids es nulo, para funciones verificar su numero de parametros
        self.ret = ret #lo que devuelve el return (si no hay return, es un void)
        self.scope = scope #nivel 

listaTSimbolos = []
numScope=1

token = TSimbolo(True, "Id", "f", "INT", None, None, None, 1)

#nodo principal arbol
nodoPadre = Node("PROGRAM")


def GetCurrentToken():
    global contador
    global curToken
    contador+=1
    global vEntrada
    global lEntrada
    if(contador<lEntrada):
        curToken=vEntrada[contador].category
        print(str(curToken))
        #print(vEntrada[contador].categoria)
        return curToken
    else:
        print("Fin de analisis")
        #sys.exit()

# def InsertSymbolTable():
#     global curToken
#     global contador
#     global vEntrada
#     global listaTSimbolos
#     tamListaTS = len(listaTSimbolos)
#     for i in tamListaTS:
#         if(listaTSimbolos[i].name !=) 
#     if()

#     token = TSimbolo(True, "Id", "f", "INT", None, None, None, 1)

def Error():
    print("ERROR SINTACTICO")
    sys.exit()

def ExpectToken(category):
    global curToken
    global vEntrada
    if(curToken == category):
        tokenNuevo = copy.copy(vEntrada[contador])
        GetCurrentToken()
        return tokenNuevo
    else:
        Error()
    
def Program(nodoPadre):
    while(curToken in pDeflist):
        Deflist(nodoPadre)

def Deflist(nodoP):
    nodo = Node("Deflist", parent=nodoP)
    DeflistP(nodo)

def DeflistP(nodoP):
    while(curToken in pDeflistP):
        nodo = Node("DeflistP", parent=nodoP)
        Def(nodo)
        DeflistP(nodo)
    
def Def(nodoP):
    if(curToken == 'IDENTIFIER'):
        nodo = Node("Def", parent=nodoP)
        Fundef(nodo)
    elif(curToken=='VAR'):
        nodo = Node("Def", parent=nodoP)
        Vardef()

def Vardef():
    ExpectToken('VAR')
    Varlist()
    ExpectToken('SEMI')

def Varlist():
    Idlist()

def Idlist():
    ExpectToken('IDENTIFIER')
    Idlistcont()

def Idlistcont():
    while(curToken in pIdlistcont):
        ExpectToken('COMMA')
        ExpectToken('IDENTIFIER')
        Idlistcont()

def Fundef(nodoP):
    global numScope
    nodoPa = Node("Fundef", parent=nodoP)
    nodo = Node("Id", parent=nodoPa)
    ExpectToken('IDENTIFIER')
    nodo2 = Node("(", parent=nodoPa)
    ExpectToken('LPAR')
    nodo3 = Node("Paramlist", parent=nodoPa)
    Paramlist(nodo3)
    nodo4 = Node(")", parent=nodoPa)
    ExpectToken('RPAR')
    nodo5 = Node("{", parent=nodoPa)
    ExpectToken('LBRACE')
    numScope+=1
    nodo6 = Node("Vardeflist", parent=nodoPa)
    Vardeflist()
    nodo7 = Node("Stmtlist", parent=nodoPa)
    Stmtlist()
    nodo8 = Node("}", parent=nodoPa)
    ExpectToken('RBRACE')
    numScope+=1

def Paramlist(nodoP):
    while(curToken in pParamlist):
        nodo = Node("Idlist", parent=nodoP)
        Idlist()

def Vardeflist():
    VardeflistP()

def VardeflistP():
    while(curToken in pVardeflistP):
        Vardef()
        VardeflistP()

def Stmtlist():
    StmtlistP()

def StmtlistP():
    while(curToken in pStmtlistP):
        Stmt()
        StmtlistP()

def Stmt():
    if(curToken in pStmtIncr):
        Stmtincr()
    elif(curToken in pStmtDecr):
        Stmtdecr()
    elif(curToken in pStmtif):
        Stmtif()
    elif(curToken in pStmtwhile):
        Stmtwhile()
    elif(curToken in pStmtdowhile):
        Stmtdowhile()
    elif(curToken in pStmtbreak):
        Stmtbreak()
    elif(curToken in pStmtreturn):
        Stmtreturn()
    elif(curToken in pStmtempty):
        Stmtempty()
    else:
        ExpectToken('IDENTIFIER')
        StmtP()

def StmtP():
    if(curToken == 'EQUAL'):
        ExpectToken('EQUAL')
        Expr()
        ExpectToken('SEMI')
    elif(curToken == 'LPAR'):
        ExpectToken('LPAR')
        Exprlist()
        ExpectToken('RPAR')
        ExpectToken('SEMI')

def Stmtincr():
    ExpectToken('INC')
    ExpectToken('IDENTIFIER')
    ExpectToken('SEMI')

def Stmtdecr():
    ExpectToken('DEC')
    ExpectToken('IDENTIFIER')
    ExpectToken('SEMI')

def Exprlist():
    while(curToken in pExprlist):
        Expr()
        Exprlistcont()

def Exprlistcont():
    while(curToken in pExprlistcont):
        ExpectToken('COMMA')
        Expr()
        Exprlistcont()

def Stmtif():
    global numScope
    ExpectToken('IF')
    ExpectToken('LPAR')
    Expr()
    ExpectToken('RPAR')
    ExpectToken('LBRACE')
    numScope+=1
    Stmtlist()
    ExpectToken('RBRACE')
    numScope+=1
    Elseiflist()
    Elsel()

def Elseiflist():
    ElseiflistP()

def ElseiflistP():
    global numScope
    while(curToken in pElseiflistP):
        ExpectToken('ELIF')
        ExpectToken('LPAR')
        Expr()
        ExpectToken('RPAR')
        ExpectToken('LBRACE')
        numScope+=1
        Stmtlist()
        ExpectToken('RBRACE')
        numScope+=1
        ElseiflistP()

def Elsel():
    global numScope 
    while(curToken in pElsel):
        ExpectToken('ELSE')
        ExpectToken('LBRACE')
        numScope+=1
        Stmtlist()
        ExpectToken('RBRACE')
        numScope+=1

def Stmtwhile():
    global numScope
    ExpectToken('WHILE')
    ExpectToken('LPAR')
    Expr()
    ExpectToken('RPAR')
    ExpectToken('LBRACE')
    numScope+=1
    Stmtlist()
    ExpectToken('RBRACE')
    numScope+=1

def Stmtdowhile():
    global numScope
    ExpectToken('DO')
    ExpectToken('LBRACE')
    numScope+=1
    Stmtlist()
    ExpectToken('RBRACE')
    numScope+=1
    ExpectToken('WHILE')
    ExpectToken('LPAR')
    Expr()
    ExpectToken('RPAR')
    ExpectToken('SEMI')

def Stmtbreak():
    ExpectToken('BREAK')
    ExpectToken('SEMI')

def Stmtreturn():
    ExpectToken('RETURN')
    Expr()
    ExpectToken('SEMI')

def Stmtempty():
    ExpectToken('SEMI')

def Expr():
    Expror()

def Expror():
    Exprand() 
    ExprorP()

def ExprorP():
    while(curToken in pExprorP):
        ExpectToken('OR')
        Exprand()
        ExprorP()
    
def Exprand():
    Exprcomp()
    ExprandP()

def ExprandP():
    while(curToken in pExprandP):
        ExpectToken('AND')
        Exprcomp()
        ExprandP()
    
def Exprcomp():
    Exprrel()
    ExprcompP()

def ExprcompP():
    while(curToken in pExprcompP):
        Opcomp()
        Exprrel()
        ExprcompP()

def Opcomp():
    if(curToken == 'EQEQUAL'):
        ExpectToken('EQEQUAL')
    else:
        ExpectToken('NOTEQUAL')

def Exprrel():
    Expradd()
    ExprrelP()

def ExprrelP():
    while(curToken in pExprrelP):
        Oprel()
        Expradd()
        ExprrelP()

def Oprel():
    if(curToken == 'LESS'):
        ExpectToken('LESS')
    elif(curToken == 'LESSEQUAL'):
        ExpectToken('LESSEQUAL')
    elif(curToken == 'GREATER'):
        ExpectToken('GREATER')
    elif(curToken == 'GREATEREQUAL'):
        ExpectToken('GREATEREQUAL')

def Expradd():
    Exprmul()
    ExpraddP()

def ExpraddP():
    while(curToken in pExpraddP):
        Opadd()
        Exprmul()
        ExpraddP()

def Opadd():
    if(curToken == 'PLUS'):
        ExpectToken('PLUS')
    elif(curToken == 'MINUS'):
        ExpectToken('MINUS')

def Exprmul():
    Exprunary()
    ExprmulP()

def ExprmulP():
    while(curToken in pExprmulP):
        Opmul()
        Exprunary()
        ExprmulP()

def Opmul():
    if(curToken == 'STAR'):
        ExpectToken('STAR')
    elif(curToken == 'SLASH'):
        ExpectToken('SLASH')
    elif(curToken == 'PERCENT'):
        ExpectToken('PERCENT')

def Exprunary():
    if(curToken in pOpunary):
        Opunary()
        Exprunary()
    else:
        Exprprimary()

def Opunary():
    if(curToken == 'PLUS'):
        ExpectToken('PLUS')
    elif(curToken == 'MINUS'):
        ExpectToken('MINUS')
    elif(curToken == 'NOT'):
        ExpectToken('NOT')
    
def Exprprimary():
    if(curToken == 'IDENTIFIER'):
        ExpectToken('IDENTIFIER')
        ExprprimaryP()
    elif(curToken in pArray):
        Array()
    elif(curToken in pLit):
        Lit()
    else:
        ExpectToken('LPAR')
        Expr()
        ExpectToken('RPAR')

def ExprprimaryP():
    while(curToken in pExprprimaryP):
        ExpectToken('LPAR')
        Exprlist()
        ExpectToken('RPAR')

def Array():
    ExpectToken('LSQB')
    Exprlist()
    ExpectToken('RSQB')

def Lit():
    if(curToken == 'TRUE'):
        ExpectToken('TRUE')
    elif(curToken == 'FALSE'):
        ExpectToken('FALSE')
    elif(curToken == 'INTEGER'):
        ExpectToken('INTEGER')
    elif(curToken == 'CHARACTER'):
        ExpectToken('CHARACTER')
    elif(curToken == 'STRING'):
        ExpectToken('STRING')

GetCurrentToken()
Program(nodoPadre)

print("\n")
print("Árbol sintáctico")
print("\n")
for pre, fill, node in RenderTree(nodoPadre):
    print("%s%s" % (pre, node.name))
