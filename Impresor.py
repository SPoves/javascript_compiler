#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 01:45:35 2020

@author: CRISGE
"""

"""
Hay que crear una tabla de tablas y luego instancias de locales y globales ¿maybe 3 clases o 3 funciones?
Crear la global al inicializar?
"""
import os
import sys

class Impresor:
    
    def  __init__(self):
        return
        
    def Gramatica(self):
        
        file = open("./Gramatica.txt", "w")
        file.write('NoTerminales = { P B T S S1 X M C H A K L Q E R R1 O O1 F F1 U }\n')
        file.write('Terminales = { let number string boolean < ; { } ( ) ++ if while return input alert = - , ! id numero cadena function eof }\n')
        file.write('Axioma = P\n')
        file.write('Producciones = {\n')
        file.write('P -> B P\n')
        file.write('P -> M P\n')
        file.write('P -> eof\n')
        file.write('B -> let T id ;\n') 
        file.write('B -> if ( E ) S\n')
        file.write('B -> while ( E ) { C }\n') 
        file.write('B -> S\n')
        file.write('T -> number\n')
        file.write('T -> string\n')
        file.write('T -> boolean\n')
        file.write('S -> alert ( E ) ;\n')
        file.write('S -> input ( id ) ;\n') 
        file.write('S -> return X ;\n')
        file.write('S -> ++  id ;\n')
        file.write('S -> id S1 ;\n')
        file.write('S1 -> = E\n')
        file.write('S1 -> ( L )\n')
        file.write('S1 -> ++\n')
        file.write('X -> E\n')
        file.write('X -> lambda\n')
        file.write('M -> function H id ( A ) { C }\n')
        file.write('C -> B C\n')
        file.write('C -> lambda\n')
        file.write('H -> T\n')
        file.write('H -> lambda\n')
        file.write('A -> T id K\n')
        file.write('A -> lambda\n')
        file.write('K -> , T id K\n')
        file.write('K -> lambda\n')
        file.write('L -> E Q\n')
        file.write('L -> lambda\n')
        file.write('Q -> , E Q\n')
        file.write('Q -> lambda\n')
        file.write('E -> ! R\n') 
        file.write('E -> R\n')
        file.write('R -> O R1\n')
        file.write('R1 -> < O\n')
        file.write('R1 -> lambda\n')
        file.write('O -> F O1\n')
        file.write('O1 -> - F\n')
        file.write('O1 -> lambda\n')
        file.write('F -> U F1\n')
        file.write('F1 -> ++\n')
        file.write('F1 -> ( L )\n')
        file.write('F1 -> lambda\n')
        file.write('U -> ( E )\n')
        file.write('U -> id\n')
        file.write('U -> cadena\n') 
        file.write('U -> numero\n')
        file.write('U -> ++ id\n') 
        file.write('}')
        file.close()
    
    def duplicates(lst, item):
        return [i for i, x in enumerate(lst) if x == item]
    
    def Tokens(self,tokens):
        
        file = open("./Tokens.txt", "w")
        
        posiciones = []
        
        for i in tokens:
            if i.clave != 'ID':
                file.write('< '+i.clave+','+i.valor+' >\n')
            
            else:
                file.write('< '+i.clave+','+str(i.posts)+' >\n')
                
        file.close()
        
    def Parse(self,parse):
        
        file = open("./Parse.txt", "w")
        file.write('descendente')
        
        for i in parse:
            file.write(' '+str(i))
        
        file.close()
        
    def Error(self, token):
        
        file = open("./Errores.txt", "w")
        file.write('Error de tipo '+ token.tipo+' en la linea '+str(token.linea)+': '+token.valor)
        file.close()
        sys.exit()
        
        # IMPRIMIR TS
        
        
        
        
    
