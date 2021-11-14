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
listaCategoria=['MULTICOM','DX','COMMENT','LPAR','RPAR','LSQB','RSQB','LBRACE','RBRACE','SEMI','COMMA','MINUS','PLUS','STAR','SLASH','PERCENT','EQEQUAL','NOTEQUAL','GREATEREQUAL','LESSEQUAL','LESS','EQUAL','GREATER','MAIN','PRINTS','AND','BREAK','DEC','DO','ELIF','ELSE','FALSE','IF','INC','NOT','OR','RETURN','TRUE','VAR','WHILE','IDENTIFIER','INTEGER','STRING','CHARACTER','CHARACTER','CHARACTER','ENTER','TAB','READLINE','SPACE','RDOUBLESLASH','CSIMPLE','CDOUBLE','ILEGAL', 'EMPTY']
listaCategoriaSimbolo=['','','','(',')','[',']','{','}',';',',','-','+','*','/','%','==','<>','>=','<=','<','=','>',"un Identifier","un Identifier",'and','break','dec','do','elif','else','false','if','inc','not','or','return','true','var','while',"un identifier","un entero","un string","un caracter","un caracter","un caracter",'enter','tab','readline','espacio','\\','\'','\"','Ilegal', 'ε']
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
            
            # if int
            #     c-1=minus
            #         if 1-2,147,483,648 
            #             chingon
            #         else
            #             F muere el programa
            #     else    
            #         if 0-2,147,483,647
            #             chingon
            #         else
            #             F print(integer fuera de rango)



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
print("Fin de análisis léxico")
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
#ε

curToken = ""

#VARIABLES PARA ERROR
lTokensDeseados=[]

#VARIABLES PARA TABLA DE SIMBOLOS

class TSimbolo:
    def __init__(self, declared, tokenType, name, dataType, size, params, ret, scope ):
        self.declared = declared #verificar si ya existia ese id o no (TRUE FALSE)
        self.tokenType = tokenType #tipo de token (variable o funcion)
        self.name = name #nombre o identificador del token
        self.dataType = dataType #si es un id, verificar su literal 
        self.size = size #algunos necesitan el tamaño
        self.params = params #si es una funcion necesitamos cantidad de parametros y el tipo de cada uno, para ids es nulo, para funciones verificar su numero de parametros
        self.ret = ret #si es una funcion(el tipo de retorno), lo que devuelve el return (si no hay return, es un void)
        self.scope = scope #nivel de contexto 

#tipo de dato en la primera asignacion
#validar los digitos del INT
listaTSimbolos = []
numScope=1


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
        #print(str(curToken))
        return curToken
    else:
        print("Fin de analisis sintáctico\n")

def ErrorS(categoria, token):
    global listaCategoriaSimbolo
    global listaCategoria
    global vEntrada
    global lEntrada
    global contador

    print("ERROR SINTACTICO\n")

    pos= listaCategoria.index(categoria)
    categoriaDeseada = listaCategoriaSimbolo[pos]

    pos2= listaCategoria.index(token)
    tokenObt = listaCategoriaSimbolo[pos2]

    if(contador==lEntrada):
        contador-=1
        tokenObt="ε"

    row = vEntrada[contador].row
    col = vEntrada[contador].column

    print("Se esperaba: " + categoriaDeseada + "\nPero se encontro: "+ tokenObt + "\nen fila: " + str(row) + "\nen columna: " + str(col))
    
    print("Arbol\n")
    for pre, fill, node in RenderTree(nodoPadre):
        print("%s%s" % (pre, node.name))

    print("Tabla de símbolos\n")

    #del tablaSimbolos[len(tablaSimbolos)-1]
    for i in range(len(tablaSimbolos)): 
        print(
            str(tablaSimbolos[i].declared) + "|" + 
            tablaSimbolos[i].tokenType + "|" + 
            tablaSimbolos[i].name  + "|" +
            tablaSimbolos[i].dataType  + "|" +
            tablaSimbolos[i].size + "|" +
            str(tablaSimbolos[i].params) + "|" +
            tablaSimbolos[i].ret + "|" +
            str(tablaSimbolos[i].scope)
            )
    
    sys.exit()

def Error(categoryList, token):
    global listaCategoriaSimbolo
    global listaCategoria
    global vEntrada
    global contador

    print("ERROR SINTACTICO\n")
    lCats=""
    for i in range(len(categoryList)):
        pos= listaCategoria.index(categoryList[i])
        categoriaDeseada = listaCategoriaSimbolo[pos]

        if i == 0:
            lCats=lCats + categoriaDeseada
        else:
            lCats=lCats + ", " + categoriaDeseada

    pos2= listaCategoria.index(token)
    tokenObt = listaCategoriaSimbolo[pos2]

    row = vEntrada[contador].row
    col = vEntrada[contador].column
    print("Se esperaba: " + lCats + "\nPero se encontro: "+tokenObt+ "\nen fila: " + str(row) + "\nen columna: " + str(col) )
    
    print("Arbol")
    for pre, fill, node in RenderTree(nodoPadre):
        print("%s%s" % (pre, node.name))

    print("Tabla de símbolos")
    #del tablaSimbolos[len(tablaSimbolos)-1]
    for i in range(len(tablaSimbolos)): 
        print(
            str(tablaSimbolos[i].declared) + "|" + 
            tablaSimbolos[i].tokenType + "|" + 
            tablaSimbolos[i].name  + "|" +
            tablaSimbolos[i].dataType  + "|" +
            tablaSimbolos[i].size + "|" +
            str(tablaSimbolos[i].params) + "|" +
            tablaSimbolos[i].ret + "|" +
            str(tablaSimbolos[i].scope)
            )
        
    sys.exit()

def ExpectToken(category):
    global curToken
    global vEntrada
    #print("curtoken"+ curToken)
    #print("contador"+str(contador))
    #print("ventrada "+vEntrada[contador-1].lexema)
    if(curToken == category):   
        print(category) 
        tokenNuevo = copy.copy(vEntrada[contador])
        GetCurrentToken()
        return tokenNuevo
    else:
        ErrorS(category,curToken)


#----------------------------------------------------------------------------------------        
#1.-Var equivalente a Parámetro, si ya esta en la tabla (id) muere, si no existe lo agrega 
#1.- Conseguir lo que devuelven las funciones, esto sinifica que hay un return, sino no tiene un return es un void
#2.- Si tiene un return tenemos que ver si es un lit o 
#Tipo de dato
tDatoToken = ""

#vEntrada
tablaSimbolos = []
boolParam = False
boolVar = False
boolFun = False
boolReturn = False
contadorParam = 0
tokenActualReturn = Token
nombreFunReturn = ""
tokenReturnCategory = ""

tokActualAssign= False
nombreVar = ""

def VerificarExistencia(token):
    global tablaSimbolos
    
def lastFunction():
    global contadorParam
    global tablaSimbolos
    newList = list(reversed(tablaSimbolos))
    
    for i in range(len(newList)): 
        if(newList[i].tokenType == "función"):
            tablaSimbolos[len(tablaSimbolos)-1-i].params = contadorParam
            break
    
#Scope
    
def crearVar(token):
    declared = VerificarExistencia(token)
    if(boolVar==True):
        objeto = TSimbolo(True, "variable", token.lexema, "*", "*", "-", "-", numScope)
    elif(boolParam==True):
        objeto = TSimbolo(True, "parametro", token.lexema, "*", "*", "-", "-", numScope)
    tablaSimbolos.append(objeto)
    
def crearFun(token):
    global contadorParam
    declared = VerificarExistencia(token)
    objeto = TSimbolo(True, "función", token.lexema, "-", "-", contadorParam, "*", numScope)
    tablaSimbolos.append(objeto)
    
def returnReturn():
    global tokenActualReturn
    global boolReturn
    global nombreFunReturn
    global tokenReturnCategory
    global tablaSimbolos
    #print(nombreFunReturn)
    for i in range(len(tablaSimbolos)):
        if(tablaSimbolos[i].name == nombreFunReturn and tablaSimbolos[i].tokenType == "función"):
            if(boolReturn == True):
                if(tokenReturnCategory == "LSQB"):
                    tablaSimbolos[i].ret = "ARRAY"
                    tokenReturnCategory = ""
                elif(tokenReturnCategory == "LPAR"):
                    tablaSimbolos[i].ret = "OPER"
                    tokenReturnCategory = ""
                elif(tokenActualReturn.category == "IDENTIFIER"):
                    tablaSimbolos[i].ret = "ID"
                elif(tokenActualReturn.category == "INTEGER"):
                    tablaSimbolos[i].ret = "INT"
                elif(tokenActualReturn.category == "CHARACTER"):
                    tablaSimbolos[i].ret = "CHAR"
                elif(tokenActualReturn.category == "STRING"):
                    tablaSimbolos[i].ret = "STRING"
                elif(tokenActualReturn.category == "TRUE" or tokenActualReturn.category == "FALSE"):
                    tablaSimbolos[i].ret = "BOOL"
            else:
                tablaSimbolos[i].ret = "0"
    
#---------------------------------------------------------------------------------------- 

def Program(nodoPadre):
    while(curToken in pDeflist):
        Deflist(nodoPadre)
    if curToken not in pDeflist:
        nodoE= Node("ε", parent=nodoPadre)

def Deflist(nodoP):
    nodo = Node("Deflist", parent=nodoP)
    DeflistP(nodo)

def DeflistP(nodoP):
    while(curToken in pDeflistP):
        nodo = Node("DeflistP", parent=nodoP)
        Def(nodo)
        DeflistP(nodo)
    if curToken not in pDeflistP:
        nodoE= Node("ε", parent=nodoP)
    
def Def(nodoP):
    nodo = Node("Def", parent=nodoP)
    if(curToken == 'IDENTIFIER'):
        Fundef(nodo)
    elif(curToken=='VAR'):
        Vardef(nodo)

def Vardef(nodoP):
    global boolVar
    boolVar = True
    nodoPa = Node("Vardef", parent=nodoP)
    nodo = Node("VAR", parent=nodoPa)
    ExpectToken('VAR')
    nodo2 = Node("Varlist", parent=nodoP)
    Varlist(nodo2)
    nodo3 = Node(";", parent=nodoP)
    boolVar = False
    ExpectToken('SEMI')

def Varlist(nodoP):
    nodo= Node("Idlist", parent=nodoP)
    Idlist(nodo)

def Idlist(nodoP):
    global contadorParam
    nodo = Node("Id", parent=nodoP)
    ExpectToken('IDENTIFIER')
    crearVar(vEntrada[contador-1])
    contadorParam+=1
    nodo2 = Node("Idlistcont", parent=nodoP)
    Idlistcont(nodo2)

def Idlistcont(nodoP):
    global contadorParam
    while(curToken in pIdlistcont):
        nodo = Node(",", parent=nodoP)
        ExpectToken('COMMA')
        nodo2= Node("Id", parent=nodoP)
        ExpectToken('IDENTIFIER')
        crearVar(vEntrada[contador-1])
        contadorParam+=1
        nodo3= Node("Idlistcont", parent=nodoP)
        Idlistcont(nodo3)
    if curToken not in pIdlistcont:
        nodoE= Node("ε", parent=nodoP)

def Fundef(nodoP):
    global numScope
    global boolParam
    global nombreFunReturn
    global boolReturn
    nodoPa = Node("Fundef", parent=nodoP)
    nodo = Node("Id", parent=nodoPa)
    ExpectToken('IDENTIFIER')
    crearFun(vEntrada[contador-1])
    nombreFunReturn = vEntrada[contador-1].lexema
    nodo2 = Node("(", parent=nodoPa)
    ExpectToken('LPAR')
    boolParam = True
    nodo3 = Node("Paramlist", parent=nodoPa)
    Paramlist(nodo3)
    boolParam = False
    nodo4 = Node(")", parent=nodoPa)
    ExpectToken('RPAR')
    nodo5 = Node("{", parent=nodoPa)
    ExpectToken('LBRACE')
    nodo6 = Node("Vardeflist", parent=nodoPa)
    Vardeflist(nodo6)
    nodo7 = Node("Stmtlist", parent=nodoPa)
    Stmtlist(nodo7)
    nodo8 = Node("}", parent=nodoPa)
    returnReturn()
    ExpectToken('RBRACE')
    boolReturn = False
    numScope+=1

def Paramlist(nodoP):
    global numScope
    global contadorParam
    numScope+=1
    contadorParam=0
    while(curToken in pParamlist):
        nodo = Node("Paramlist", parent=nodoP)
        Idlist(nodo)
    lastFunction()
    if curToken not in pParamlist:
        nodoE= Node("ε", parent=nodoP)

def Vardeflist(nodoP):
    nodo = Node("Vardeflist", parent=nodoP)
    VardeflistP(nodo)

def VardeflistP(nodoP):
    while(curToken in pVardeflistP):
        nodo = Node("VardeflistP", parent=nodoP)
        Vardef(nodo)
        VardeflistP(nodo)
    if curToken not in pVardeflistP:
        nodoE= Node("ε", parent=nodoP)

def Stmtlist(nodoP):
    nodo = Node("Stmtlist", parent=nodoP)
    StmtlistP(nodo)

def StmtlistP(nodoP):
    global contador
    global lEntrada
    global vEntrada
    global curToken

    if (curToken in pStmtlistP and contador == lEntrada):
        curToken="EMPTY"
    while(curToken in pStmtlistP ):
        nodo = Node("StmtlistP", parent=nodoP)
        Stmt(nodo)
        StmtlistP(nodo)
    if curToken not in pStmtlistP:
        nodoE= Node("ε", parent=nodoP)

def Stmt(nodoP):
    global nombreVar
    if curToken not in pStmt:
        Error(pStmt,curToken)
    else:
        nodo = Node("Stmt", parent=nodoP)
        if(curToken in pStmtIncr):
            Stmtincr(nodo)
        elif(curToken in pStmtDecr):
            Stmtdecr(nodo)
        elif(curToken in pStmtif):
            Stmtif(nodo)
        elif(curToken in pStmtwhile):
            Stmtwhile(nodo)
        elif(curToken in pStmtdowhile):
            Stmtdowhile(nodo)
        elif(curToken in pStmtbreak):
            Stmtbreak(nodo)
        elif(curToken in pStmtreturn):
            Stmtreturn(nodo)
        elif(curToken in pStmtempty):
            Stmtempty(nodo)
        else:
            nodo2 = Node("Id", parent=nodoP)
            nombreVar = vEntrada[contador].lexema
            ExpectToken('IDENTIFIER')
            nodo3 = Node("StmtP", parent=nodoP)
            StmtP(nodo3)

def StmtP(nodoP):
    global nombreVar
    global tokActualAssign
    if curToken not in pStmtP:
        Error(pStmtP,curToken)
    else:
        if(curToken == 'EQUAL'):
            #ASIGNACIONES
            nodo = Node("=", parent=nodoP)
            ExpectToken('EQUAL')
            nodo2 = Node("Expr", parent=nodoP)
            tokActualAssign = True
            Expr(nodo2)
            for pre, fill, node in RenderTree(nodo2):
                if(tokActualAssign==True):
                    for i in range(len(tablaSimbolos)):
                        if(tablaSimbolos[i].declared == TRUE):
                            if(tablaSimbolos[i].name == nombreVar and (tablaSimbolos[i].tokenType == "parametro" or tablaSimbolos[i].tokenType == "variable") ):
                                if(node.name=="array"):
                                    tablaSimbolos[i].ret = "ARRAY"
                                    #print("ARRAY")
                                    #print(tablaSimbolos[i].name)
                                    tokActualAssign=False
                                    break
                                elif(node.name=="Id"):
                                    #verificar si es funcion o variable
                                    tablaSimbolos[i].ret = "ID"
                                    #print("FUNCTION")
                                    break
                                elif(node.name=="integer"):
                                    tablaSimbolos[i].ret = "INT"
                                    #print("INTEGER")
                                    break
                                elif(node.name=="character"):
                                    tablaSimbolos[i].ret = "CHAR"
                                    #print("CHARACTER")
                                    break
                                elif(node.name=="bool"):
                                    tablaSimbolos[i].ret = "BOOL"
                                    #print("BOOLEAN")
                                    break
                                elif(node.name=="string"):
                                    tablaSimbolos[i].ret = "STRING"
                                    #print("STRING")
                                    break
                                                      
                #print("%s%s" % (pre, node.name))

            nodo3 = Node(";", parent=nodoP)
            ExpectToken('SEMI')
        elif(curToken == 'LPAR'):
            #LLAMAR FUNCIONES SIN GUARDAR VALOR
            nodo4 = Node("(", parent=nodoP)
            ExpectToken('LPAR')
            nodo5 = Node("Exprlist", parent=nodoP)
            Exprlist(nodo5)
            nodo6 = Node(")", parent=nodoP)
            ExpectToken('RPAR')
            nodo7 = Node(";", parent=nodoP)
            ExpectToken('SEMI')

def Stmtincr(nodoP):
    nodoPa = Node("Stmtincr", parent=nodoP) 
    nodo = Node("inc", parent=nodoPa)
    ExpectToken('INC')
    nodo2 = Node("Id", parent=nodoPa)
    ExpectToken('IDENTIFIER')
    nodo3 = Node(";", parent=nodoPa)
    ExpectToken('SEMI')

def Stmtdecr(nodoP):
    nodoPa = Node("Stmtdecr", parent=nodoP)
    nodo = Node("dec", parent=nodoPa)
    ExpectToken('DEC')
    nodo2 = Node("Id", parent=nodoPa)
    ExpectToken('IDENTIFIER')
    nodo3 = Node(";", parent=nodoPa)
    ExpectToken('SEMI')

def Exprlist(nodoP):
    while(curToken in pExprlist):
        nodo = Node("Exprlist", parent=nodoP)
        Expr(nodo)
        Exprlistcont(nodo)
    if curToken not in pExprlist:
        nodoE= Node("ε", parent=nodoP)

def Exprlistcont(nodoP):
    while(curToken in pExprlistcont):
        nodo = Node(",", parent=nodoP)
        ExpectToken('COMMA')
        nodo2 = Node("Exprlistcont", parent=nodoP)
        Expr(nodo2)
        Exprlistcont(nodo2)
    if curToken not in pExprlistcont:
        nodoE= Node("ε", parent=nodoP)

def Stmtif(nodoP):
    global numScope
    nodoPa = Node("Stmtif", parent=nodoP)
    nodo = Node("if", parent=nodoPa)
    ExpectToken('IF')
    nodo2 = Node("(", parent=nodoPa)
    ExpectToken('LPAR')
    nodo3 = Node("Expr", parent=nodoPa)
    Expr(nodo3)
    nodo4 = Node(")", parent=nodoPa)
    ExpectToken('RPAR')
    nodo5 = Node("{", parent=nodoPa)
    ExpectToken('LBRACE')
    numScope+=1
    nodo6 = Node("Stmtlist", parent=nodoPa)
    Stmtlist(nodo6)
    nodo7 = Node("}", parent=nodoPa)
    ExpectToken('RBRACE')
    numScope+=1
    nodo8 = Node("Elseiflist", parent=nodoPa)
    Elseiflist(nodo8)
    nodo9 = Node("Else", parent=nodoPa)
    Elsel(nodo9)

def Elseiflist(nodoP):
    nodo = Node("ElseiflistP", parent=nodoP)
    ElseiflistP(nodo)

def ElseiflistP(nodoP):
    global numScope
    while(curToken in pElseiflistP):
        nodo = Node("elif", parent=nodoP)
        ExpectToken('ELIF')
        nodo2 = Node("(", parent=nodoP)
        ExpectToken('LPAR')
        nodo3 = Node("Expr", parent=nodoP)
        Expr(nodo3)
        nodo4 = Node(")", parent=nodoP)
        ExpectToken('RPAR')
        nodo5 = Node("{", parent=nodoP)
        ExpectToken('LBRACE')
        numScope+=1
        nodo6 = Node("Stmtlist", parent=nodoP)
        Stmtlist(nodo6)
        nodo7 = Node("}", parent=nodoP)
        ExpectToken('RBRACE')
        numScope+=1
        nodo8 = Node("EsleiflistP", parent=nodoP)
        ElseiflistP(nodo8)
    if curToken not in pElseiflistP:
        nodoE= Node("ε", parent=nodoP)

def Elsel(nodoP):
    global numScope 
    while(curToken in pElsel):
        nodo = Node("else", parent=nodoP)
        ExpectToken('ELSE')
        nodo2 = Node("{", parent=nodoP)
        ExpectToken('LBRACE')
        numScope+=1
        nodo3 = Node("Stmtlist", parent=nodoP)
        Stmtlist(nodo3)
        nodo4 = Node("}", parent=nodoP)
        ExpectToken('RBRACE')
        numScope+=1
    if curToken not in pElsel:
        nodoE= Node("ε", parent=nodoP)

def Stmtwhile(nodoP):
    global numScope
    nodoPa = Node("Stmtwhile", parent=nodoP)
    nodo = Node("while", parent=nodoPa)
    ExpectToken('WHILE')
    nodo2 = Node("(", parent=nodoPa)
    ExpectToken('LPAR')
    nodo3 = Node("Expr", parent=nodoPa)
    Expr(nodo3)
    nodo4 = Node(")", parent=nodoPa)
    ExpectToken('RPAR')
    nodo5 = Node("}", parent=nodoPa)
    ExpectToken('LBRACE')
    numScope+=1
    nodo6 = Node("Stmtlist", parent=nodoPa) 
    Stmtlist(nodo6)
    nodo7 = Node("}", parent=nodoPa)
    ExpectToken('RBRACE')
    numScope+=1

def Stmtdowhile(nodoP):
    global numScope
    nodoPa = Node("Stmtdowhile", parent=nodoP)
    nodo = Node("do", parent=nodoPa)
    ExpectToken('DO')
    nodo2 = Node("{", parent=nodoPa)
    ExpectToken('LBRACE')
    numScope+=1
    nodo3 = Node("Stmtlist", parent=nodoPa)
    Stmtlist(nodo3)
    nodo4 = Node("}", parent=nodoPa)
    ExpectToken('RBRACE')
    numScope+=1
    nodo5 = Node("while", parent=nodoPa)
    ExpectToken('WHILE')
    nodo6 = Node("(", parent=nodoPa)
    ExpectToken('LPAR')
    nodo7 = Node("Expr", parent=nodoPa)
    Expr(nodo7)
    nodo8 = Node(")", parent=nodoPa)
    ExpectToken('RPAR')
    nodo9 = Node(";", parent=nodoPa)
    ExpectToken('SEMI')

def Stmtbreak(nodoP):
    nodoPa = Node("Stmtbreak", parent=nodoP)
    nodo = Node("break", parent=nodoPa)
    ExpectToken('BREAK')
    nodo2 = Node(";", parent=nodoPa)
    ExpectToken('SEMI')

def Stmtreturn(nodoP):
    global boolReturn
    boolReturn = True
    nodoPa = Node("Stmtreturn", parent=nodoP)
    nodo = Node("return", parent=nodoPa)
    ExpectToken('RETURN')
    nodo2 = Node("Expr", parent=nodoPa)
    Expr(nodo2)
    nodo3 = Node(";", parent=nodoPa)
    ExpectToken('SEMI')

def Stmtempty(nodoP):
    nodoPa = Node(";", parent=nodoP)
    nodo = Node(";", parent=nodoPa)
    ExpectToken('SEMI')

def Expr(nodoP):
    nodo = Node("Expror", parent=nodoP)
    Expror(nodo)

def Expror(nodoP):
    nodo = Node("Exprand", parent=nodoP)
    Exprand(nodo) 
    nodo2 = Node("ExprorP", parent=nodoP)
    ExprorP(nodo2)

def ExprorP(nodoP):
    while(curToken in pExprorP):
        nodo = Node("or", parent=nodoP)
        ExpectToken('OR')
        nodo2 = Node("Exprand", parent=nodoP)
        Exprand(nodo2)
        nodo3 = Node("ExprorP", parent=nodoP)
        ExprorP(nodo3)
    if curToken not in pExprorP:
        nodoE= Node("ε", parent=nodoP)
    
def Exprand(nodoP):
    nodo = Node("Exprcomp", parent=nodoP)
    Exprcomp(nodo)
    nodo2 = Node("ExprandP", parent=nodoP)
    ExprandP(nodo2)

def ExprandP(nodoP):
    while(curToken in pExprandP):
        nodo = Node("and", parent=nodoP)
        ExpectToken('AND')
        nodo2 = Node("Exprcomp", parent=nodoP)
        Exprcomp(nodo2)
        nodo3 = Node("ExprandP", parent=nodoP)
        ExprandP(nodo3)
    if curToken not in pExprandP:
        nodoE= Node("ε", parent=nodoP)
    
def Exprcomp(nodoP):
    nodo = Node("Exprrel", parent=nodoP)
    Exprrel(nodo)
    nodo2 = Node("ExprcompP", parent=nodoP)
    ExprcompP(nodo2)

def ExprcompP(nodoP):
    while(curToken in pExprcompP):
        nodo = Node("Opcomp", parent=nodoP)
        Opcomp(nodo)
        nodo2 = Node("Exprrel", parent=nodoP)
        Exprrel(nodo2)
        nodo3 = Node("ExprcompP", parent=nodoP)
        ExprcompP(nodo3)
    if curToken not in pExprcompP:
        nodoE= Node("ε", parent=nodoP)

def Opcomp(nodoP):
    if curToken not in pOpcomp:
        Error(pOpcomp,curToken)
    else:
        if(curToken == 'EQEQUAL'):
            nodo = Node("==", parent=nodoP)
            ExpectToken('EQEQUAL')
        else:
            nodo2 = Node("<>", parent=nodoP)
            ExpectToken('NOTEQUAL')

def Exprrel(nodoP):
    nodo = Node("Expradd", parent=nodoP)
    Expradd(nodo)
    nodo2 = Node("ExprrelP", parent=nodoP)
    ExprrelP(nodo2)

def ExprrelP(nodoP):
    while(curToken in pExprrelP):
        nodo = Node("Oprel", parent=nodoP)
        Oprel(nodo)
        nodo2 = Node("Expradd", parent=nodoP)
        Expradd(nodo2)
        nodo3 = Node("ExprrelP", parent=nodoP)
        ExprrelP(nodo3)
    if curToken not in pExprrelP:
        nodoE= Node("ε", parent=nodoP)

def Oprel(nodoP):
    if curToken not in pOprel:
        Error(pOprel,curToken)
    else:
        if(curToken == 'LESS'):
            nodo = Node("<", parent=nodoP)
            ExpectToken('LESS')
        elif(curToken == 'LESSEQUAL'):
            nodo2 = Node("<=", parent=nodoP)
            ExpectToken('LESSEQUAL')
        elif(curToken == 'GREATER'):
            nodo3 = Node(">", parent=nodoP)
            ExpectToken('GREATER')
        elif(curToken == 'GREATEREQUAL'):
            nodo4 = Node(">=", parent=nodoP)
            ExpectToken('GREATEREQUAL')

def Expradd(nodoP):
    nodo = Node("Exprmul", parent=nodoP)
    Exprmul(nodo)
    nodo2 = Node("ExpraddP", parent=nodoP)
    ExpraddP(nodo2)

def ExpraddP(nodoP):
    while(curToken in pExpraddP):
        nodo = Node("Opadd", parent=nodoP)
        Opadd(nodo)
        nodo2 = Node("Exprmul", parent=nodoP)
        Exprmul(nodo2)
        nodo3 = Node("ExpraddP", parent=nodoP)
        ExpraddP(nodo3)
    if curToken not in pExpraddP:
        nodoE= Node("ε", parent=nodoP)

def Opadd(nodoP):
    if curToken not in pOpadd:
        Error(pOpadd,curToken)
    else:
        if(curToken == 'PLUS'):
            nodo = Node("+", parent=nodoP)
            ExpectToken('PLUS')
        elif(curToken == 'MINUS'):
            nodo2 = Node("-", parent=nodoP)
            ExpectToken('MINUS')

def Exprmul(nodoP):
    nodo = Node("Exprunary", parent=nodoP)
    Exprunary(nodo)
    nodo2 = Node("ExprmulP", parent=nodoP)
    ExprmulP(nodo2)

def ExprmulP(nodoP):
    while(curToken in pExprmulP):
        nodo = Node("Opmul", parent=nodoP)
        Opmul(nodo)
        nodo2 = Node("Exprunary", parent=nodoP)
        Exprunary(nodo2)
        nodo3 = Node("ExprmulP", parent=nodoP)
        ExprmulP(nodo3)
    if curToken not in pExprmulP:
        nodoE= Node("ε", parent=nodoP)

def Opmul(nodoP):
    if curToken not in pOpmul:
        Error(pOpmul,curToken)
    else:
        if(curToken == 'STAR'):
            nodo = Node("*", parent=nodoP)
            ExpectToken('STAR')
        elif(curToken == 'SLASH'):
            nodo2 = Node("/", parent=nodoP)
            ExpectToken('SLASH')
        elif(curToken == 'PERCENT'):
            nodo3 = Node("%", parent=nodoP)
            ExpectToken('PERCENT')

def Exprunary(nodoP):
    if curToken not in pExprunary:
        Error(pExprunary,curToken)
    else:
        if(curToken in pOpunary):
            nodo = Node("Opunary", parent=nodoP)
            Opunary(nodo)
            nodo2 = Node("Exprunary", parent=nodoP)
            Exprunary(nodo2)
        else:
            nodo3 = Node("Exprprimary", parent=nodoP)
            Exprprimary(nodo3)

def Opunary(nodoP):
    if curToken not in pOpunary:
        Error(pOpunary,curToken)
    else:
        if(curToken == 'PLUS'):
            nodo = Node("+", parent=nodoP)
            ExpectToken('PLUS')
        elif(curToken == 'MINUS'):
            nodo2 = Node("-", parent=nodoP)
            ExpectToken('MINUS')
        elif(curToken == 'NOT'):
            nodo3 = Node("not", parent=nodoP)
            ExpectToken('NOT')
    
def Exprprimary(nodoP):
    global vEntrada
    global contador
    global tokenActualReturn
    global tokenReturnCategory
    
    if curToken not in pExprprimary:
        Error(pExprprimary,curToken)
    else:
        if(curToken == 'IDENTIFIER'):
            tokenActualReturn = vEntrada[contador]
            nodo = Node("Id", parent=nodoP)
            ExpectToken('IDENTIFIER')
            nodo2 = Node("ExprprimaryP", parent=nodoP)
            ExprprimaryP(nodo2)
        elif(curToken in pArray):
            tokenReturnCategory = "LSQB"
            nodo3 = Node("array", parent=nodoP)
            Array(nodo3)
        elif(curToken in pLit):
            tokenActualReturn = vEntrada[contador]
            nodo4 = Node("lit", parent=nodoP)
            Lit(nodo4)
        else:
            tokenReturnCategory = "LPAR"
            nodo5 = Node("(", parent=nodoP)
            ExpectToken('LPAR')
            nodo6 = Node("Expr", parent=nodoP)
            Expr(nodo6)
            nodo7 = Node(")", parent=nodoP)
            ExpectToken('RPAR')

def ExprprimaryP(nodoP):
    while(curToken in pExprprimaryP):
        nodo = Node("(", parent=nodoP)
        ExpectToken('LPAR')
        nodo2 = Node("Exprlist", parent=nodoP)
        Exprlist(nodo2)
        nodo3 = Node(")", parent=nodoP)
        ExpectToken('RPAR')
    if curToken not in pExprprimaryP:
        nodoE= Node("ε", parent=nodoP)

def Array(nodoP):
    nodo = Node("[", parent=nodoP)
    ExpectToken('LSQB')
    nodo2 = Node("Exprlist", parent=nodoP)
    Exprlist(nodo2)
    nodo3 = Node("]", parent=nodoP)
    ExpectToken('RSQB')

def Lit(nodoP):
    if curToken not in pLit:
        Error(pLit,curToken)
    else:
        if(curToken == 'TRUE'):
            nodo = Node("bool", parent=nodoP)
            ExpectToken('TRUE')
        elif(curToken == 'FALSE'):
            nodo2 = Node("bool", parent=nodoP)
            ExpectToken('FALSE')
        elif(curToken == 'INTEGER'):
            nodo3 = Node("integer", parent=nodoP)
            ExpectToken('INTEGER')
        elif(curToken == 'CHARACTER'):
            nodo4 = Node("character", parent=nodoP)
            ExpectToken('CHARACTER')
        elif(curToken == 'STRING'):
            nodo5 = Node("string", parent=nodoP)
            ExpectToken('STRING')

GetCurrentToken()
Program(nodoPadre)

print("\n")
print("Árbol sintáctico")
print("\n")
for pre, fill, node in RenderTree(nodoPadre):
    print("%s%s" % (pre, node.name))

print("Tabla de símbolos")
for i in range(len(tablaSimbolos)): 
    print(
        str(tablaSimbolos[i].declared) + "|" + 
        tablaSimbolos[i].tokenType + "|" + 
        tablaSimbolos[i].name  + "|" +
        tablaSimbolos[i].dataType  + "|" +
        tablaSimbolos[i].size + "|" +
        str(tablaSimbolos[i].params) + "|" +
        tablaSimbolos[i].ret + "|" +
        str(tablaSimbolos[i].scope)
        )