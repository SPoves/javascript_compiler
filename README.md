# Compiler

Ejemplo de un compilador Javascript (no todas las opciones han sido implementadas).

Se compone de tres analizadores (léxico, sintáctico y semántico), una tabla de símbolos y un gestor de errores, que son capaces de procesar el texto y devolver los siguientes ficheros de texto. 

- Tokens generados por el analizador léxico a partir del codigo javascript. (Tokens.txt)
- Gramatica utilizada por el compilador (Gramatica.txt)
- Reglas gramaticales utilizadas por el compilador para reconocer el texto. (Parse.txt)
- Tablas de Simbolos globales y locales (TS.txt)
- Si hay errores fichero de errores (Errores.txt)

Para ejecutar en Windows:

- Descargar Principal.exe
- En cmd ir al directorio donde se encuentre Principal.exe
- Ejecutar: Principal path/fichero_javascript.js

Para ejecutar en mac:

- Descargar Principal (Ejecutable Unix) 
- En la terminal ir al directorio donde se encuentra Principal
- Ejecutar: ./Principal path/fichero_javascript.js

