#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 00:28:55 2020

@author: CRISGE
"""

import os

# ElemTS

class Elem:
    
    def __init__(self,valor,tipo,desplazamiento,parametro): 

        self.valor=valor
        self.tipo=tipo
        self.desplazamiento=desplazamiento
        self.parametro=parametro
        self.funcion=False

class Fun:
    
    def __init__(self,valor,tiporetorno,tipos,parametros): 
        
        self.valor=valor
        self.tiporetorno=tiporetorno
        self.tipos=tipos
        self.funcion=True

class TS:
    
    def __init__(self,existe,tipo,nombre,contador):
        
        self.elementos=[]
        self.desplazamiento=0
        self.existe=existe
        self.tipo = tipo
        self.nombre = nombre
        self.contador = contador
        self.posts=0
        
    def desplazamiento(self,valor):
        
        self.desplazamiento+=valor
    
    # TSG
    def imprimirTSG(self, lista):
        
        file = open("./TS.txt", "w")
        file.write('TABLA PRINCIPAL\n')
        
        for i in self.elementos:
            
            file.write("\n")
            
            # Imprimimos funcion
            if i.funcion:
              
                file.write("LEXEMA: \'"+i.valor+"\' ( funcion )\n")
                file.write("ATRIBUTOS:\n")
                file.write('+ tipoRet : '+i.tiporetorno+'\n' )
                file.write('+ numParam: '+str(len(i.tipos))+'\n' )
                
                for a in range(len(i.tipos)):
                   file.write("+ TipoParam"+str(a)+": "+i.tipos[a]+"\n" ) 
                
            # Imprimimos variable
            else:
                
                file.write("LEXEMA: \'"+i.valor+"\' ( variable )\n")
                file.write('+ tipo : '+i.tipo +'\n')
                file.write('+ despl : '+str(i.desplazamiento) +'\n')    
        
        cont = 1
        
        for i in lista:
            
            file.write("\n")
            file.write("----------------------------------------------------\n")
            file.write("\n")
            
            file.write('TABLA de la FUNCIÓN '+i['nombre']+' #'+str(cont)+':\n')
            cont=cont+1
            
            file.write("\n")
            
            for j in i['elementos']:
                param="\'variable\'"
                if j.parametro:
                    param="\'parametro\'"
            
                file.write("LEXEMA: \'"+j.valor+"\' ( "+param+" )\n")
                file.write('+ tipo : '+j.tipo+'\n' )
                file.write('+ despl : '+str(j.desplazamiento)+'\n' )
                   
        file.close()
     
        
    def buscar(self,token):
        
        for i in self.elementos:
            
            if token.valor==i.valor and not i.funcion:
                return True
        
        return False
    
    def buscarFun(self,token):
        
        for i in self.elementos:
            
            if token.valor==i.valor and i.funcion:
                return i
        
        return 'null'
    
    def encontrar(self,token):
        
        
        for i in self.elementos:
            if token.valor==i.valor and not i.funcion:
                return i
            
        return 'null'
    
    def encontrarF(self,token):
        
        
        for i in self.elementos:
            if token.valor==i.valor and i.funcion:
                return i
            
        return 'null'
    
    def parametros(self):
        
        contador=0
        
        for i in self.elementos:
            if i.parametro:
                contador+=1
        
        return contador
    
    def parametrosI(self,ind):
        
        contador=0
        for i in self.elementos:
            if i.parametro:
                contador=contador+1
            if contador == ind:
                return i.tipo
    
    def lisParam():
        
        lista=[]
        
        for i in self.elementos:
            
            if i.parametro:
                lista=lista+[i]
        
        return lista
        
    '''      
    def meterElem(self,token,tipo):
        
        elemento=Elem(token.valor,token.tipo)
        
        
        
            self.TSL.elementos = self.TSL.elementos + [self.actual]
        
        
    def meterFun():
        return 0
        
     '''   
        
        
        
        
        
        
        
        
        
        
        
        
        