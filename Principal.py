#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 01:45:44 2020

@author: CRISGE
"""

import re
import sys
from Lexico import Lexico
from SintSem import SintSem
from Impresor import Impresor

############### FUNCIONES ###############

""" FUNCION COMENTARIOS """
""" Elimina los comentarios del texto """

def comentarios(texto):
    
    coments = re.findall('\/\*.*?\*\/',texto,re.DOTALL)

    for i in coments:
        
        enters = i.count('\n')
        
        # Cambiamos coment por nada 
        texto=texto.replace(i,'\n'*enters)
        
    return texto

##########################################
    
####### PROCESAMIENTO DE TEXTO ###########
    


# LECTURA
    
#if len(sys.argv)<2:

   # err = open("./Errores.txt","w")
   # err.write("Se esperaba un fichero como parametro de entrada.")
   # err.close()
   # sys.exit()
    
#file = open(sys.argv[1],"r")
file = open('prueba.js',"r")
text = file.read()
file.close()
 

# SUSTITUIMOS TEMPORALMENTE LAS CADENAS

cadenas = re.findall('\".*?\"',text)
tempCad = re.sub('\".*?\"','_Aqui_Habia_Una_Cadenita_',text)

# ELIMINAMOS LOS COMENTARIOS

text = comentarios(tempCad)

# VOLVEMOS A PONER LAS CADENAS

for i in cadenas:
    text = text.replace('_Aqui_Habia_Una_Cadenita_',i,1) 
   
# SEPARACION POR LINEAS Y GUARDADO
#### Array con pares 
#### (CONTENIDO, NUMERO)

lines = text.split("\n")
for i in range(len(lines)):
    
    if lines[i]!='':
        lines[i] = (lines[i],i+1)

# Eliminamos lineas en blanco
lines[:]= (value for value in lines if value!='')


##########################################



# llamada lexico (texto)
    #devuelve array tokens/errores -> hay que hacerlo aun (crreo que podemos llamarlo como atrib del obj clase)

lex=Lexico(lines)
tokens=lex.tkSem


# IMPRIMIR GRAMATICA

imp = Impresor()
imp.Gramatica()

# llamada sintactico (array tokens/errores)
    # devuelve parse
""" sint sem() 
    siguiente()
    P()
    """
a=SintSem(tokens)
actual=a.siguiente()

imp.Tokens(a.lexico)
imp.Parse(a.parse)



































