
#Lenguje de Programacion (KOTLIN)

# Integrantes
# DIAZ CEDEÑO JAHIR ALEXANDER
# SALTOS HERNANDEZ NOELIA ALEJANDRA
# SANTACRUZ GOROZABEL CRISTHIAN MAICKEL


import ply.lex as lex
import os
from datetime import datetime


# Lista de tokens para nuestro lexer
tokens = [

    #Comienzo Cristhian Santacruz
   
    'NUMBER_INT',      
    'NUMBER_DOUBLE',   
    'STRING',          
    
    # Identificadores
    'ID',            

    'PLUS',            # +
    'MINUS',           # -
    'MULTIPLY',        # *
    'DIVIDE',          # /
    'MODULO',          # %
    
  
    'ASSIGN',          # =
    'EQUALS',          # ==
    'NOT_EQUALS',      # !=
    'GREATER_EQUAL',   # >=
    'LESS_EQUAL',      # <=
    'GREATER',         # >
    'LESS',            # <
    
  
    'AND',             # &&
    'OR',              # ||
    
    
    'QUESTION',        # ?
    'ELVIS',           # ?:
    
   
    'LPAREN',          # (
    'RPAREN',          # )
    'LBRACE',          # {
    'RBRACE',          # }
    'SEMICOLON',       # ;
    'COMMA',           # ,
    'COLON',           # :
    
    # Fin Cristhian Santacruz
    #Noelia Saltos Hernandez
    'RANGE',
    #Fin Noelia Saltos Hernandez

]

# Palabras reservada del lenguaje kotlin
reserved = {

    #Inicio Cristhian Santacruz

    'val': 'VAL',           # Declaracion de variable inmutable/constante
    'var': 'VAR',           # Declaracion para variables mutables
    'fun': 'FUN',           # Declaracion de función
    'return': 'RETURN',    
    'when': 'WHEN',         # Estructura de selección múltiple de koklin
    'Int': 'TYPE_INT',     
    'Double': 'TYPE_DOUBLE',
    'Boolean': 'TYPE_BOOLEAN', 
    'String': 'TYPE_STRING',   
    'true': 'BOOLEAN_TRUE',    
    'false': 'BOOLEAN_FALSE',  
    'println': 'PRINTLN', 
    # Fin Cristhian Santacruz

    #Noelia Saltos Hernandez
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    #Fin Noelia Saltos Hernandez
   
}


tokens = tokens + list(reserved.values())

# Reglas para tokens simples (un solo carácter)
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'
t_QUESTION = r'\?'

# Reglas para tokens 

#Noelia Saltos Hernandez

# Comentario de una línea
def t_COMMENT_LINE(t):
    r'\/\/.*'
    pass  # Se ignora

# Comentario de múltiples líneas
def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_RANGE(t):
    r'\.\.'
    return t

# Fin Noelia Saltos Hernandez

# Inicio Cristhian Santacruz
def t_ELVIS(t):
    r'\?\:'
    return t

def t_EQUALS(t):
    r'=='
    return t

def t_NOT_EQUALS(t):
    r'!='
    return t

def t_GREATER_EQUAL(t):
    r'>='
    return t

def t_LESS_EQUAL(t):
    r'<='
    return t

def t_GREATER(t):
    r'>'
    return t

def t_LESS(t):
    r'<'
    return t

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_NUMBER_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
    return t

# Fin Cristhian Santacruz

# Regla para identificadores 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Regla para ell conteo de las lineas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados (espacios y tabs)
t_ignore = ' \t'

# Manejo de errores -Noelia Saltos Hernandez
def t_error(t):
    error_msg = f"Carácter incorrecto '{t.value[0]}' en línea {t.lineno}"
    print(error_msg)

    if hasattr(t.lexer, "log_file") and t.lexer.log_file:
        t.lexer.log_file.write("ERROR: " + error_msg + "\n")

    t.lexer.skip(1)


# Aqui contruimos el lexer
lexer = lex.lex()

#Noelia Saltos Hernandez
# Función para probar el lexer con un código de ejemplo

def test_lexer(data, usuario_git="usuarioGit"):
    lexer.input(data)
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")
    filename = f"logs/lexico-{usuario_git}-{timestamp}.txt"

    os.makedirs("logs", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as log_file:
        log_file.write("=== LOG DE ANALISIS LEXICO ===\n")
        log_file.write(f"Usuario: {usuario_git}\n")
        log_file.write(f"Fecha y hora: {timestamp}\n\n")
        log_file.write("Tokens reconocidos:\n")

        lexer.log_file = log_file  # <- Para que el t_error lo pueda usar

        while True:
            tok = lexer.token()
            if not tok:
                break
            token_info = f"Token: {tok.type} - Valor: {repr(tok.value)} - Línea actual : {tok.lineno}"
            print(token_info)
            log_file.write(token_info + "\n")

        log_file.write("\nFin del análisis léxico.\n")
        log_file.write("================================\n")

def analizar_archivo(nombre_archivo, usuario_git="usuarioGit"):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            test_lexer(contenido, usuario_git)
    except FileNotFoundError:
        print(f"❌ El archivo {nombre_archivo} no fue encontrado.")


if __name__ == "__main__":
    print("=== ANALIZADOR LEXICO KOTLIN-LIKE ===\n")


    # Analizar archivo externo .kt
    analizar_archivo("algoritmo2.kt", usuario_git="NoeSaltos")
