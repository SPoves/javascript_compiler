#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 01:46:04 2020

@author: CRISGE
"""

from Token import Token
import re

#Recibe el texto en un array por lineas y devuelve un array de tokens
    
class Lexico:
    
    """
    CONSTRUCTOR
    Llama a buscador
    Añade los nuevos tokens a un array de tokens
    """
    
    
    def __init__(self,text):
        
        self.tkSem=[]  
        self.text=text
        for i in self.text: 
            self.tkSem=self.tkSem+self.buscador(i)

        

    """
    BUSCADOR
    Recibe una linea y devuelve un array con los tokens de la linea
    """
    
    def buscador(self,linea):
        
        tokens=[]
 
        # IDENTIFICACION TOKENS #
        # 1. Eliminamos el token de linea
        # 2. Creamos el nuevo token 
        # 3. Añadimos el token al array
        
        while not re.search('^\s*$',linea[0]):

            linea=(re.sub('\s*','',linea[0],1),linea[1])
            
            if re.match('\(',linea[0]):
                
                linea=(linea[0].replace('(','',1),linea[1])
                token = Token('PARA','(',linea[1],'','')
                tokens=tokens+[token]
        
            # )
            elif re.match('\)',linea[0]):
                
                linea=(linea[0].replace(')','',1),linea[1])
                token = Token('PARC',')',linea[1],'','')
                tokens=tokens+[token]
        
            # =
            elif re.match('=',linea[0]):
                
                linea=(linea[0].replace('=','',1),linea[1])
                token = Token('ASIG','=',linea[1],'','')
                tokens=tokens+[token]
        
            # -
            elif re.match('-',linea[0]):
                
                linea=(linea[0].replace('-','',1),linea[1])
                token = Token('RES','-',linea[1],'','')
                tokens=tokens+[token]
        
            # !
            elif re.match('!',linea[0]):
                
                linea=(linea[0].replace('!','',1),linea[1])
                token = Token('NEG','!',linea[1],'','')
                tokens=tokens+[token]
        
            # ++
            elif re.match('\+\+',linea[0]):
                
                linea=(linea[0].replace('++','',1),linea[1])
                token = Token('INC','++',linea[1],'','')
                tokens=tokens+[token]
        
            # {
            elif re.match('{',linea[0]):
                
                linea=(linea[0].replace('{','',1),linea[1])
                token = Token('CORA','{',linea[1],'','')
                tokens=tokens+[token]
        
            # }
            elif re.match('}',linea[0]):
                
                linea=(linea[0].replace('}','',1),linea[1])
                token = Token('CORC','}',linea[1],'','')
                tokens=tokens+[token]
        
            # <
            elif re.match('<',linea[0]):
                
                linea=(linea[0].replace('<','',1),linea[1])
                token = Token('MENOR','<',linea[1],'','')
                tokens=tokens+[token]
            
            # ,
            elif re.match(',',linea[0]):
                
                linea=(linea[0].replace(',','',1),linea[1])
                token = Token('COMA',',',linea[1],'','')
                tokens=tokens+[token]
            
            # ;
            elif re.match(';',linea[0]):
                
                linea=(linea[0].replace(';','',1),linea[1])
                token = Token('PYC',';',linea[1],'','')
                tokens=tokens+[token]
            
            # NUMERO
            elif re.match('\d+',linea[0],re.ASCII):
                
                num=re.findall('\d+',linea[0],re.ASCII)
                linea=(re.sub('\d+','',linea[0],1),linea[1])
                if int(num[0])<=32767:
                    token = Token('NUM',num[0],linea[1],'','')
                else:
                    token = Token('ERROR','El maximo numero admitido es 32767.',linea[1],'Lexico','')
                tokens=tokens+[token]
                
            # CADENA
            elif re.match('\".*?\"',linea[0]):
                
                cad=re.findall('\".*?\"',linea[0])
                linea=(re.sub('\".*?\"','',linea[0],1),linea[1])
                if len(cad)>66:
                    token = Token('ERROR','Las cadenas no pueden contener mas de 64 caracteres.',linea[1],'Lexico','')
                else:    
                    token = Token('CAD',cad[0],linea[1],'','')
                tokens=tokens+[token]
                
                
            # PR o ID
            elif linea[0][0].isalpha():
                
                #let = re.findall('\w+',linea[0],re.ASCII)
                let = re.findall('\w+',linea[0])

                linea=(re.sub('\w+','',linea[0],1),linea[1])
                
                pr = ['let', 'number', 'boolean', 'string', 'while', 'if', 'alert', 'input', 'return', 'function']
                
                # Si es PR
                if pr.count(let[0])>0:
                    token = Token('PR',let[0],linea[1],'','')
                # Si no es PR es ID
                else:
                    token = Token('ID',let[0],linea[1],'','')
                tokens=tokens+[token]
            else:
                
                token = Token('ERROR','No se reconoce el caracter '+linea[0][0] ,linea[1],'Lexico','')
                linea=(re.sub('.','',linea[0],1,re.DOTALL),linea[1])
                tokens=tokens+[token]
        
        return tokens
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
        

