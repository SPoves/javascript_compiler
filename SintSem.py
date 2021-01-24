#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 01:46:13 2020

@author: CRISGE
"""


# hay que añadir parametros a los errores

from Token import Token
from Impresor import Impresor
from ElemTS import TS
from ElemTS import Elem
from ElemTS import Fun

class SintSem:
    
    ####################### BUSCA UNICO #######################
    ####### Comprueba los tokens que se van a imprimir ########
    ###########################################################
    
    def buscaUnico(self,valor):
        
        for i in self.lexico:
            
            if i.valor==valor:
                return True
        
        return False
    
    ####################### SIGUIENTE #######################
    ### Llama a la lista de tokens recibida por el lexico ###
    #########################################################
    
    def siguiente(self):
        
        if len(self.tokens)>0:
            self.actual = self.tokens.pop(0)
            
        else:
            token = Token('EOF','_',self.actual.linea,'','')
            self.tokens = self.tokens + [token]
            self.actual = token
            return
        
        if not self.buscaUnico(self.actual.valor) :
            self.lexico = self.lexico + [self.actual]
            
        if self.actual.clave=='ERROR':
            token = Token('ERROR',self.actual.valor,self.actual.linea,'Lexico','')
            self.imp.Error(token)
        
    ##################### DESPLAZAMIENTO ######################
    ### Calcula el desplazamiento segun el tipo de variable ### 
    ###########################################################
    
    def desplazamiento(self,tipo):
    # El desplazamiento se ha hecho en bytes (2 bytes = 1 palabra)
    
        if tipo == 'number':
            return 2
            
        elif tipo == 'string':
            return 128
        
        elif tipo == 'boolean':
            return 2
        else:
            token = Token('ERROR','Se esperaba number, string o boolean pero se ha recibido '+tipo,self.actual.linea,'Sintactico','')
            self.imp.Error(token)
        return

    ##################### BUSCAID #####################
    ### Mete la posts en el array de tokens final #####
    ###################################################
    
    def buscaID(self, token, posTS):
        
        long = len(self.lexico)-1
        for i in range(long):
            
            # Sacamos todos los indices de los ids con posts vacia y rellenamos todos con el ultimo
            
            if self.lexico[long-i].clave =='ID' and self.lexico[long-i].posts =='':
                self.lexico[long-i].posts = posTS
        
        
        
    ############################ PRODUCCIONES ################################

    def P(self):
        
    # 1 P -> B P
        first=['let','if','while','alert','input','id','++','return']
        if first.count(self.actual.valor)>0 or self.actual.clave=='ID':
            
            self.parse.append(1)
            self.B()
            
            self.P()
            
            
            
     # 2 P -> M P       
        elif self.actual.valor=='function':
  
            self.parse.append(2)
            
            self.M()
            
            self.P()
            
    # 3 P -> EOF
        elif self.actual.clave=='EOF':

            self.parse.append(3)
            self.TSG.imprimirTSG(self.listaTSL)
            
            return
        
        else:
            
            # Hacer un token y llamar a errores
            token = Token('ERROR','No se admite el token '+self.actual.valor+' al inicio de sentencia.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
            
    
    def B(self):
    
        first=['alert','input','id','++','return']
        
    # 4 B -> let T id; 
        if self.actual.valor=='let':
        
            self.parse.append(4)
        
            self.siguiente()
        
            tipoVar = self.T()
        
          ### Comprobar ID
            if(self.actual.clave=='ID'): 
                
                # Tabla LOCAL
                if self.TSL.existe:
                
                    # Si existia lanzamos error
                    if self.TSL.buscar(self.actual):
                        token = Token('ERROR',': El identificador '+self.actual.valor+' ya ha sido declarado en la funcion.',self.actual.linea,'Semantico','')
                        self.imp.Error(token)
                        
                    # Si no existia lo metemos
                    else:
                        
                        elem = Elem(self.actual.valor,tipoVar,self.TSG.desplazamiento,False)
                        self.TSL.elementos = self.TSL.elementos + [elem]
                        self.TSL.desplazamiento = self.TSL.desplazamiento + self.desplazamiento(tipoVar)
                        self.TSL.posts = self.TSL.posts + 1
                        self.actual.posts = self.TSL.posts
                        self.buscaID(self.actual, self.actual.posts)
                        
                # Tabla GLOBAL
                else:
                    
                    # Si existia lanzamos error
                    if self.TSG.buscar(self.actual):
                        token = Token('ERROR',': El identificador '+self.actual.valor+' ya ha sido declarado en el ambito global.',self.actual.linea,'Semantico','')
                        self.imp.Error(token)
                        
                    # Si no existia lo metemos
                    else:
                        
                        elem = Elem(self.actual.valor,tipoVar,self.TSG.desplazamiento,False)
                        self.TSG.elementos = self.TSG.elementos + [elem]
                        self.desplazamiento('number')
                        self.TSG.desplazamiento = self.TSG.desplazamiento + self.desplazamiento(tipoVar)
                        self.TSG.posts = self.TSG.posts + 1
                        self.actual.posts = self.TSG.posts
                        self.buscaID(self.actual, self.actual.posts)
                            
            else: 
                token = Token('ERROR','Se esperaba un identificador y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
          ### Fin comprobar id
          
            self.siguiente()
        
            if self.actual.valor!=';':
                token = Token('ERROR','Se esperaba un ; y se ha recibido '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
                
            self.siguiente()
            
            
    # 5 B -> if (E) S 
        elif self.actual.valor=='if':
            self.parse.append(5)
            
            self.siguiente()
            
            if self.actual.valor!='(':
                token = Token('ERROR','Se esperaba un ( y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
            tipoExp = self.E()
        
        # Semantico
            if tipoExp != 'boolean':
                token = Token('ERROR','Se esperaba una expresion de tipo booleano en la condicion de la sentencia if pero se ha recibido una de tipo '+tipoExp,self.actual.linea,'Semantico','')
                self.imp.Error(token)          
        # Semantico    
                
            if self.actual.valor!=')':
                token = Token('ERROR','Se esperaba un ) y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
                
            self.siguiente()
            self.S()
            
    # 6 B -> while (E){ C } 
        elif self.actual.valor=='while':
            self.parse.append(6)
            
            self.siguiente()
            
            if self.actual.valor!='(':
                token = Token('ERROR','Se esperaba un ( y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
            tipoExp = self.E()
        
        # Semantico
            if tipoExp != 'boolean':
                token = Token('ERROR','Se esperaba una expresion de tipo booleano en la condicion de la sentencia while pero se ha recibido una de tipo '+tipoExp,self.actual.linea,'Semantico','')
                self.imp.Error(token)          
        # Semantico    
                
            if self.actual.valor!=')':
                token = Token('ERROR','Se esperaba un ) y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
                
            if self.actual.valor!='{':
                token = Token('ERROR','Se esperaba un { y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
                
            self.C()
                
            if self.actual.valor!='}':
                token = Token('ERROR','Se esperaba un } y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
                
            self.siguiente()
                
    # 7 B -> S
        elif self.actual.clave=='ID' or first.count(self.actual.valor)>0:
            self.parse.append(7)
        
            self.S()
        
        else: 
            token = Token('ERROR','No se admite el token '+self.actual.valor+' al inicio de sentencia.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
            
            
    def T(self):
        
    # 8 T -> number 
        if self.actual.valor == 'number':
            self.parse.append(8)
            
            self.siguiente()
            
            return 'number'
            
    # 9 T -> string 
        elif self.actual.valor == 'string':
            self.parse.append(9)
            
            self.siguiente()

            return 'string'
            
    # 10 T -> boolean
        elif self.actual.valor == 'boolean':
            self.parse.append(10)
            
            self.siguiente()
            
            return 'boolean'
            
        else:
            token = Token('ERROR','No se reconoce el token '+self.actual.valor+' como tipo de variable.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
    
    def S(self):
        
    # 11 S -> alert ( E ) ; 
        if self.actual.valor == 'alert':
            self.parse.append(11)
            
            self.siguiente()
            
            if self.actual.valor!='(':
                token = Token('ERROR','Se esperaba un ( y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
            tipoExp=self.E()
            
            # Semantico
            if tipoExp != 'string' and 'number'!= tipoExp:
                token = Token('ERROR','Se esperaba una expresion de tipo cadena o int en la sentencia alert pero se ha recibido una de tipo '+tipoExp,self.actual.linea,'Semantico','')
                self.imp.Error(token)          
            # Semantico 
            
            if self.actual.valor!=')':
                token = Token('ERROR','Se esperaba un ) y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
                
            self.siguiente()
            
            if self.actual.valor!=';':
                token = Token('ERROR','Se esperaba un ; y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
    # 12 S -> input ( id ) ; 
        elif self.actual.valor == 'input':
            self.parse.append(12)
            self.siguiente()
            
            if self.actual.valor!='(':
                token = Token('ERROR','Se esperaba un ( y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
      
            if(self.actual.clave!='ID'):
                token = Token('ERROR','Se esperaba un identificador en la sentencia input pero se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            # Semantico: Comprobacion TS
            
            if not self.TSL.buscar(self.actual) and not self.TSG.buscar(self.actual):
                
                # Si no esta ni en la local ni en la global lo declaramos como global de tipo number               
                elem = Elem(self.actual.valor,'number',self.TSG.desplazamiento,False)
                self.TSG.elementos = self.TSG.elementos + [elem]
                self.TSG.desplazamiento = self.TSG.desplazamiento + 2
                self.TSG.posts = self.TSG.posts + 1
                self.actual.posts = self.TSG.posts
                self.buscaID(self.actual, self.actual.posts)
                
            # Semantico: Tipos
            
            if self.TSL.buscar(self.actual):
                elem = self.TSL.encontrar(self.actual)
            else:
                elem = self.TSG.encontrar(self.actual)
            
            if elem.tipo != 'string' and 'number'!= elem.tipo:
                token = Token('ERROR','Se esperaba una expresion de tipo cadena o int en la sentencia alert pero se ha recibido una de tipo '+tipoExp,self.actual.linea,'Semantico','')
                self.imp.Error(token) 
                
            # Fin Semantico
        
            self.siguiente()
            
            if self.actual.valor!=')':
                token = Token('ERROR','Se esperaba un ) y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
                
            self.siguiente()
            
            if self.actual.valor!=';':
                token = Token('ERROR','Se esperaba un ; y se ha recibido '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
    # 13 S -> return X ; 
        elif self.actual.valor == 'return':
            self.parse.append(13)
            
            if not self.TSL.existe:
                token = Token('ERROR','La sentencia return no esta permitida fuera de una funcion.',self.actual.linea,'Semantico','')
                self.imp.Error(token)
                
            self.siguiente()
            
            tipoRet=self.X()
            
            # Semantico: Comprobación tipo funcion
            
            if tipoRet != self.TSL.tipo:
                token = Token('ERROR','La funcion es de tipo '+self.TSL.tipo +' pero se ha recibido '+tipoRet+' en la sentencia return.',self.actual.linea,'Semantico','')
                self.imp.Error(token)
            
            # Fin Semantico
            
            #self.siguiente() -> se llama desde X
            
            if self.actual.valor!=';':
                token = Token('ERROR','Se esperaba un ; y se ha recibido '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
                
            self.siguiente()
            
            
    # 14 S -> ++  id ; 
        elif self.actual.valor == '++':
            self.parse.append(14)
            
            self.siguiente()
            
            if self.actual.clave != 'ID':
                
                token = Token('ERROR','Se esperaba un identificador pero se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            # Semantico: buscar en TS
            if not self.TSL.buscar(self.actual) and not self.TSG.buscar(self.actual):
                
                # Si no esta ni en la local ni en la global lo declaramos como global de tipo number               
                elem = Elem(self.actual.valor,'number',self.TSG.desplazamiento,False)
                self.TSG.elementos = self.TSG.elementos + [elem]
                self.TSG.desplazamiento = self.TSG.desplazamiento + 2
                self.TSG.posts = self.TSG.posts + 1
                self.actual.posts = self.TSG.posts
                self.buscaID(self.actual, self.actual.posts)
                    
            # Semantico: Comprobar tipo
            
            
            elem = self.TSL.encontrar(self.actual)
            if elem=='null':
                elem = self.TSG.encontrar(self.actual)
                
            if elem.tipo != 'number':
                token = Token('ERROR','Se esperaba un identificador de tipo number pero se ha recibido uno de tipo: '+elem.tipo,self.actual.linea,'Semantico','')
                self.imp.Error(token)
            
            # Fin Semantico
            
            self.siguiente()
            
            if self.actual.valor!=';':
                token = Token('ERROR','Se esperaba un ; y se ha recibido '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
    # 15 S -> id S1 ;
        elif self.actual.clave == 'ID':
            self.parse.append(15)

            identificador = Token(self.actual.clave, self.actual.valor, self.actual.linea, self.actual.tipo, self.actual.posts)

            self.siguiente()
            
            
            tipo = self.S1()
            
            ### Semantico: Funcion
            if tipo[0]=='funcion':
                
                elem=self.TSG.encontrarF(identificador)
                
                if elem=='null' or not elem.funcion:
                    token = Token('ERROR','La funcion '+identificador.valor+' no ha sido declarada.',self.actual.linea,'Semantico','')
                    self.imp.Error(token)
                
                tipo.pop(0)
                
                tiposFun = elem.tipos
                
                if len(tipo) != len(tiposFun):
                    token = Token('ERROR','Se esperaban '+len(tipo)+' parametros pero se han recibido '+len(elem.tipos)+'.',self.actual.linea,'Semantico','')
                    self.imp.Error(token)
   
                for i in range(len(tipo)):
                    
                    if tipo[i] != tiposFun[i]:
                        token = Token('ERROR','Se esperaban un parametro de tipo '+tipo[i]+' pero se ha recibido uno de tipo '+tiposFun[i]+'.',self.actual.linea,'Semantico','')
                        self.imp.Error(token)
             
            ### Semantico: Expresion
            
            else:
                if not self.TSL.buscar(identificador) and not self.TSG.buscar(identificador):
                    # Si no esta ni en la local ni en la global lo declaramos como global de tipo number               
                    elem = Elem(identificador.valor,'number',self.TSG.desplazamiento,False)
                    self.TSG.elementos = self.TSG.elementos + [elem]
                    self.TSG.desplazamiento = self.TSG.desplazamiento + 2
                    self.TSG.posts = self.TSG.posts + 1
                    identificador.posts = self.TSG.posts
                    self.buscaID(identificador, identificador.posts)

                elem=self.TSL.encontrar(identificador)
                if elem=='null':
                    elem=self.TSG.encontrar(identificador)
                    
                if tipo != elem.tipo:
                    token = Token('ERROR','Los tipos de la expresion no coinciden.',self.actual.linea,'Sintactico','')
                    self.imp.Error(token)
                    
            ##### Fin Semantico   
            
            
  
            if self.actual.valor!=';':
                token = Token('ERROR','Se esperaba un ; y se ha recibido '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
        else:
            token = Token('ERROR','No se admite el token '+self.actual.valor+' al inicio de sentencia.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)            
    
    
    def S1(self):
        
    # 16 S1 -> = E 
        if self.actual.valor == '=':
            self.parse.append(16)
            
            self.siguiente()
            
            tipoVar=self.E()
            
            return tipoVar
            
    # 17 S1 -> ( L ) 
        elif self.actual.valor == '(':
            self.parse.append(17)
            
            self.siguiente()
            
            parametros=self.L()

            
            if self.actual.valor!=')':
                token = Token('ERROR','Se esperaba un ) y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
                
            self.siguiente()
            
            return ['funcion'] + parametros
            
    # 18 S1 -> ++
        elif self.actual.valor == '++':
            self.parse.append(18)
            
            self.siguiente()
            
            return 'number'
            
        else:
            token = Token('ERROR','No se admite el token '+self.actual.valor+' detras de un identificador.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)            
                
    
    def X(self): 
        
        first=['!','++','(']
        firstK=['CAD','NUM','ID']

    # 19 X -> E 
        if firstK.count(self.actual.clave)>0 or first.count(self.actual.valor)>0:
            self.parse.append(19)
            
            tipoRet=self.E()
            
            
            
            return tipoRet
        
    # 20 X -> lambda
        elif self.actual.valor == ';':
            self.parse.append(20)
            
            return 'void'
        
        else:
            token = Token('ERROR','No se admite el token '+self.actual.valor+' como retorno de funcion.',self.actual.linea,'Sintactico','')
            self.imp.Error(token) 
            
    def M(self):
    # 21 M -> function H id ( A ) { C } 
        if self.actual.valor == 'function':
            self.parse.append(21)
            
            self.siguiente()
            
            tipo=self.H()
  
            if self.actual.clave!='ID':
                token = Token('ERROR','Se esperaba un identificador pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token) 
            
            # Semantico: ID funcion
            # Si ya existe una funcion con ese id -> error
            
            if self.TSL.buscarFun(self.actual.valor) != 'null':
                token = Token('ERROR','El nombre de funcion '+self.actual.valor+' ha sido utilizado anteriormente.',self.actual.linea,'Semantico','')
                self.imp.Error(token) 
            
            # Semantico: Crear TSL
            
            self.TSL.existe=True
            self.TSL.tipo=tipo
            self.TSL.nombre=self.actual.valor
            self.TSL.contador=self.TSL.contador+1
            self.TSG.posts = self.TSG.posts + 1
            identificador = Token(self.actual.clave, self.actual.valor, self.actual.linea, self.actual.tipo,self.TSG.posts)
            
            # Fin Semantico
            
            self.siguiente()

            if self.actual.valor!='(':
                token = Token('ERROR','Se esperaba un ( pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token) 
            
            self.siguiente()
            
            # Los parametros se declaran en las producciones
            parametros=self.A()
            
            if self.actual.valor!=')':
                token = Token('ERROR','Se esperaba un ) pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token) 
            
            self.siguiente()
            
            # Semantico: meter en TSG
            # Cogemos los nombres de los parametros y los tipos de la TSL
            
            tipos=[]
            parametros=[]
            
            for i in self.TSL.elementos:
                
                tipos=tipos+[i.tipo]
                parametros=parametros+[i.valor]
            
            #self.TSL.tipos = tipos
            funcion=Fun(self.TSL.nombre,self.TSL.tipo,tipos,parametros)
            self.TSG.elementos=self.TSG.elementos+[funcion]
            self.buscaID(identificador, identificador.posts)
            
            # Fin Semantico
            
            if self.actual.valor!='{':
                token = Token('ERROR','Se esperaba un { pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token) 
            
            self.siguiente()
            
            self.C()
            
            if self.actual.valor!='}':
                token = Token('ERROR','Se esperaba un } pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token) 
                
            self.siguiente()
    
            # Semantico: borrar e imprimir TSL
            
            self.listaTSL.append({'nombre': self.TSL.nombre,'elementos': self.TSL.elementos, 'tipo' : self.TSL.tipo})
            
            self.TSL.existe=False
            self.TSL.elementos=[]
            self.TSL.desplazamiento=0
            self.TSL.tipo = ''
            self.TSL.nombre = ''
            self.TSL.posts = 0
    
            # Fin Semantico
    
    def C(self):
        
    # 22 C -> B C 
        first=['let','if','while','alert','input','id','++','return']
        follow=first+['}']
        if first.count(self.actual.valor)>0 or self.actual.clave=='ID':
            self.parse.append(22)
            
            self.B()
            
            self.C()
            
    # 23 C -> lambda
        elif follow.count(self.actual.valor)>0 or self.actual.clave=='ID':
            self.parse.append(23)
    
        else:
            token = Token('ERROR','7No se admite el token '+self.actual.valor+' al inicio de sentencia.',self.actual.linea,'Sintactico','')
            self.imp.Error(token) 
            
    def H(self):
        
    # 24 H -> T 
        first=['number','string','boolean']
        if first.count(self.actual.valor)>0:
            self.parse.append(24)
            
            tipo = self.T()
            
            return tipo
            
    # 25 H -> lambda
        elif self.actual.clave=='ID':
            self.parse.append(25)
            
            return 'void'
            
        else: 
            token = Token('ERROR','No se admite el token '+self.actual.valor+' como tipo de función.',self.actual.linea,'Sintactico','')
            self.imp.Error(token) 
            
    def A(self):
        first = ['number','string','boolean']
        
    # 26 A -> T id K 
        if first.count(self.actual.valor)>0:
            self.parse.append(26)
            
            tipo = self.T()
            
            if self.actual.clave != 'ID':
                token = Token('ERROR','Se esperaba un identificador pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token) 
                
            if self.TSL.buscar(self.actual):
                token = Token('ERROR','El parametro '+self.actual.valor+' ya ha sido declarado en esta funcion.',self.actual.linea,'Sintactico','')
                self.imp.Error(token) 
            else:

                elem = Elem(self.actual.valor,tipo,self.TSL.desplazamiento,True)
                self.TSL.elementos = self.TSL.elementos + [elem]
                self.TSL.desplazamiento = self.TSG.desplazamiento + self.desplazamiento(tipo)
                self.TSL.posts = self.TSL.posts + 1
                self.actual.posts = self.TSL.posts
                self.buscaID(self.actual, self.actual.posts)
                    
            self.siguiente()
            
            self.K()
    
    # 27 A -> lambda
        elif self.actual.valor == ')':
            self.parse.append(27)
        
        else:
            token = Token('ERROR','No se admite el token '+self.actual.valor+' como parametro de función.',self.actual.linea,'Sintactico','')
            self.imp.Error(token) 
            
    def K(self):
        
        follow=[')',',']
        
    # 28 K -> , T id K
        if self.actual.valor==',':
            self.parse.append(28)
            
            self.siguiente()
            
            tipo = self.T()
            
            if self.TSL.buscar(self.actual):
                token = Token('ERROR','El parametro '+self.actual.valor+' ya ha sido declarado en esta funcion.',self.actual.linea,'Semantico','')
                self.imp.Error(token) 
            else:
                elem = Elem(self.actual.valor,tipo,self.TSL.desplazamiento,True)
                self.TSL.elementos = self.TSL.elementos + [elem]
                self.TSL.desplazamiento = self.TSL.desplazamiento + self.desplazamiento(tipo)
                self.TSL.posts = self.TSL.posts + 1
                self.actual.posts = self.TSL.posts
                self.buscaID(self.actual, self.actual.posts)
                    
            self.siguiente()
            
            self.K()
            
    
    # 29 K ->  lambda
        elif follow.count(self.actual.valor)>0:
            self.parse.append(29)
            
        else:
            token = Token('ERROR','Se ha recibido el token '+self.actual.valor+' cuando se esperaba ; o ,.',self.actual.linea,'Sintactico','')
            self.imp.Error(token) 
            
    def L(self):
        
        first=['!','++','(']
        firstK=['ID','CAD','NUM']

    # 30 L -> E Q 
        if first.count(self.actual.valor)>0 or firstK.count(self.actual.clave)>0:
            self.parse.append(30)

            tipo = self.E()
            
            parametros=self.Q()
         
            parametros = [tipo] + parametros
                    
            return parametros


    # 31 L -> lambda
        elif self.actual.valor==')':
            self.parse.append(31)
            
            return []
            
        else:
            token = Token('ERROR','Se ha recibido el token '+self.actual.valor+' cuando se esperaba una expresion o identificador.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
    
    def Q(self):
        
        follow=[',',')']

    # 32 Q -> , E Q 
        if self.actual.valor==',':
            self.parse.append(32)
            
            self.siguiente()
            
            tipo=self.E()
            
            parametros=self.Q()
            
            return [tipo] + parametros
            
    # 33 Q -> lambda
        elif follow.count(self.actual.valor)>0:
            self.parse.append(33)
         
            return []
            
        else:
            token = Token('ERROR','No se admite el token '+self.actual.valor+' como nombre de parametro.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)            
            
    def E(self):
        
        first=['ID','CAD','NUM']
        
    # 34 E -> ! R 
        if self.actual.valor=='!':
            self.parse.append(34)
            
            self.siguiente()
            
            tipo=self.R()
            
            if tipo != 'boolean':
                token = Token('ERROR','Se esperaba una expresion de tipo boolean pero se ha recibido uno de tipo '+tipo+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token)  
            
            return 'boolean'
        
    # 35 E -> R 
        elif self.actual.valor=='(' or self.actual.valor=='++' or first.count(self.actual.clave)>0:
            self.parse.append(35)
            
            tipo = self.R()
          
            return tipo
    
        else:
            token = Token('ERROR','Se ha recibido el token '+self.actual.valor+' en una expresión.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
    
    def R(self):
        
        first=['ID','CAD','NUM']
    
    # 37 R -> O R1
        if self.actual.valor=='(' or self.actual.valor=='++' or first.count(self.actual.clave)>0:
            self.parse.append(36)
            
            tipoO=self.O()
          
            tipoR=self.R1()
           
            if tipoO==tipoR:
                return 'boolean'
            
            elif tipoR=='void':
                return tipoO
            
            else:
                token = Token('ERROR','Los tipos de la expresion no coinciden.',self.actual.linea,'Semantico','')
                self.imp.Error(token)
            
        else:
            token = Token('ERROR','Se ha recibido el token '+self.actual.valor+' en una expresión.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
    
    def R1(self):
        
        follow=[',',')',';']
        
    # 38 R1 -> < O 
        if self.actual.valor=='<':
            self.parse.append(37)
            
            self.siguiente()
            
            tipo = self.O()
            
            if tipo != 'number':
                token = Token('ERROR','Se esperaba un token de tipo number pero se ha recibido uno de tipo '+tipo,self.actual.linea,'Semantico','')
                self.imp.Error(token)
                
            return 'number'
             
    # 39 R1 -> lambda
        elif follow.count(self.actual.valor)>0:
            self.parse.append(38)
        
            return 'void'
        
        else:
            token = Token('ERROR','El token '+self.actual.valor+' no es admitido en la expresion expresion.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
            
    def O(self):
        
        first=['ID','CAD','NUM']
        
    # 40 O -> F O1
        if self.actual.valor=='(' or self.actual.valor=='++' or first.count(self.actual.clave)>0:
            self.parse.append(39)
    
            tipoF=self.F()
            tipoO=self.O1()
            
            if tipoF==tipoO:
                return tipoF
            
            elif tipoO=='void':
                return tipoF
            
            else:
                token = Token('ERROR','Los tipos de la expresion no coinciden.',self.actual.linea,'Semantico','')
                self.imp.Error(token)
            
        else:
            token = Token('ERROR','El token '+self.actual.valor+' no es admitido en la expresion expresion.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
    
    def O1(self):
#puede k este follow este mal
        follow=['<',',',';',')']

    # 41 O1 -> - F 
        if self.actual.valor=='-':
            self.parse.append(40)
            
            self.siguiente()
            
            tipo = self.F()
            
            if tipo!='number':
                token = Token('ERROR','Se esperaba un token de tipo number pero se ha recibido uno de tipo '+tipo,self.actual.linea,'Semantico','')
                self.imp.Error(token)
             
            return 'number'
        
    # 42 O1 -> lambda
        elif follow.count(self.actual.valor)>0 :
            self.parse.append(41)
            
            return 'void'
    
        else:
            token = Token('ERROR','El token '+self.actual.valor+' no es admitido en la expresion expresion.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
            
    def F(self):
        
    # 43 F -> U F1 
        first=['ID','NUM','CAD']
        if self.actual.valor=='(' or self.actual.valor=='++' or first.count(self.actual.clave)>0:
            self.parse.append(42)
            
            tipoU=self.U() # no necesariamente tiene que ser un tipo puede ser un id y hay que guardar el tipo en 
            
            tipoF=self.F1()
            
            if tipoF[0]=='funcion':
                
                tipoF.pop(0)
                
                if tipoU[0] != 'id':
                    token = Token('ERROR','La expresion es incorrecta.',self.actual.linea,'Sintactico','')
                    self.imp.Error(token)
               
                funts=self.TSG.buscarFun(tipoU[1])
                
                
                if funts=='null':
                    token = Token('ERROR','No se ha declarado la funcion'+tipoU[1].actual.valor+'.',tipoU[1].actual.linea,'Semantico','')
                    self.imp.Error(token)
                
                else:
                    
                    # Comprobamos los parametros
                    
                    if len(tipoF) != len(funts.tipos):
                        token = Token('ERROR','Se esperaban '+str(len(funts.tipos))+' parametros pero se han recibido '+str(len(tipoF))+'.',tipoU[1].linea,'Semantico','')
                        self.imp.Error(token)
                    
                    for i in range(len(tipoF)):
                        if tipoF[i]!=funts.tipos[i]:
                            token = Token('ERROR','Se esperaba un parametro de tipo '+funts.tipos[i]+' parametros pero se ha recibido uno de tipo'+tipoF[i]+'.',tipoU[1].actual.linea,'Semantico','')
                            self.imp.Error(token)
                    
                    # Devolver tipo funcion
                    return funts.tiporetorno
                
                
            else:
                # comprobaciones con expresion
                
                if tipoU[0]=='id':
                    
                    #ComprobacionesTS
                    if not self.TSL.buscar(tipoU[1]) and not self.TSG.buscar(tipoU[1]):
                    
                        # Si no esta ni en la local ni en la global lo declaramos como global de tipo number               
                        elem = Elem(tipoU[1].valor,'number',self.TSG.desplazamiento,False)
                        self.TSG.elementos = self.TSG.elementos + [elem]
                        self.TSG.desplazamiento = self.TSG.desplazamiento + 2
                        self.TSG.posts = self.TSG.posts + 1
                        tipoU[1].posts = self.TSG.posts
                        
                        
                        self.buscaID(tipoU[1], tipoU[1].posts)
                        
                
## N0 le estoy pasando un token sino un string creo por eso falla
                
                    elem=self.TSL.encontrar(tipoU[1])
                    if elem=='null':
                        elem=self.TSG.encontrar(tipoU[1])
                
                    tipoU=elem.tipo
                
                if tipoF==tipoU:
                    return tipoU
            
                elif tipoF=='void':
                    return tipoU
            
                else:
                    token = Token('ERROR','Los tipos de la expresion no coinciden.',self.actual.linea,'Semantico','')
                    self.imp.Error(token)
    
        else:
           token = Token('ERROR','Se ha recibido el token '+self.actual.valor+' cuando se esperaba un id, cadena o numero.',self.actual.linea,'Sintactico','')
           self.imp.Error(token)
           
    def F1(self):
      
        follow=['-','<',';',')',',']
            
    # 44 F1 -> ++ 
        if self.actual.valor=='++':
            self.parse.append(43)
            
            self.siguiente()
            
            return 'number'
    
    # 45 F1 -> ( L )
        elif self.actual.valor=='(':
            self.parse.append(44)
            
            self.siguiente()
            
            parametros=self.L()
            
            if self.actual.valor != ')':
                token = Token('ERROR','Se esperaba ) pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
            
            return ['funcion'] + parametros
    
    # 46 F1 -> lambda
        elif follow.count(self.actual.valor)>0:
            self.parse.append(45)
     
            return 'void'
        
        else:
            token = Token('ERROR','El token '+self.actual.valor+' es incorrecto en la expresion.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
    
    def U(self):
        
    # 47 U -> ( E ) 
        if self.actual.valor=='(':
            self.parse.append(46)
            
            self.siguiente()
            
            tipo=self.E()
      
            if self.actual.valor!=')':
                token = Token('ERROR','Se esperaba un ) y se ha recibido: '+self.actual.valor,self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
            self.siguiente()
     
            return tipo
    
    # 48 U -> id 
        elif self.actual.clave=='ID':
            self.parse.append(47)
            
            identificador=Token(self.actual.clave,self.actual.valor,self.actual.linea,self.actual.tipo,'')
            
            self.siguiente()
     
            return ['id',identificador]
 
    # 49 U -> cadena 
        elif self.actual.clave=='CAD':
            self.parse.append(48)
            
            self.siguiente()
            
            return 'string'
    
    # 50 U -> numero
        elif self.actual.clave=='NUM':
            self.parse.append(49)
            
            self.siguiente()
    
            return 'number'
                    
    # 50 E -> ++ id 
        elif self.actual.valor=='++':
            self.parse.append(50)
            
            self.siguiente()
            
            if self.actual.clave != 'ID':
                token = Token('ERROR','Se esperaba un identificador pero se ha recibido '+self.actual.valor+'.',self.actual.linea,'Sintactico','')
                self.imp.Error(token)
            
             # Semantico: buscar en TS
            if not self.TSL.buscar(self.actual) and not self.TSG.buscar(self.actual):
                
                # Si no esta ni en la local ni en la global lo declaramos como global de tipo number               
                elem = Elem(self.actual.valor,'number',self.TSG.desplazamiento,False)
                self.TSG.elementos = self.TSG.elementos + [elem]
                self.TSG.desplazamiento = self.TSG.desplazamiento + 2
                self.TSG.posts = self.TSG.posts + 1
                self.actual.posts = self.TSG.posts
                
                self.buscaID(self.actual, self.actual.posts)
            
            elem = self.TSL.encontrar(self.actual)
            if elem=='null':
                elem = self.TSG.encontrar(self.actual)
                
            if elem.tipo != 'number':
                token = Token('ERROR','Se esperaba un identificador de tipo number pero se ha recibido uno de tipo: '+elem.tipo,self.actual.linea,'Semantico','')
                self.imp.Error(token)
                
            self.siguiente()

            return 'number'
        
        else:
            token = Token('ERROR','Se ha recibido el token '+self.actual.valor+' cuando se esperaba un identificador una cadena o un numero.',self.actual.linea,'Sintactico','')
            self.imp.Error(token)
            
   # def main(self):
        
        
        #a=SintSem()
        
    def __init__(self,tokens):
        
        self.lexico=[]
        self.parse=[]
        self.tokens=tokens
        self.imp = Impresor()
        self.TSG = TS(True,'Global','Global',0)
        self.TSL = TS(False,'','',0)
        self.listaTSL = []
        
        self.siguiente()
        self.P()


        
