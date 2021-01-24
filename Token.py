#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 01:46:28 2020

@author: CRISGE
"""

class Token:
    
    """ 
    Cada token tendra:
	 - Palabra Clave que indica el tipo de token
	 - Valor del token que es la cadena real
	 - Linea del fichero donde se encuentra el token originalmente
	 - Tipo (puede ser null), para el semántico
	 - PosTS, solo se usa con los Ids se mete -1 por defecto y se rellena en gramatica
    """
    
    def __init__(self, clave, valor, linea, tipo, posts):
        
        self.clave=clave
        self.valor=valor
        self.linea=linea
        self.tipo=tipo
        self.posts=posts
        return
    