
#Lenguje de Programacion (KOTLIN)

# Integrantes
# DIAZ CEDEÑO JAHIR ALEXANDER
# SALTOS HERNANDEZ NOELIA ALEJANDRA
# SANTACRUZ GOROZABEL CRISTHIAN MAICKEL


import ply.lex as lex

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

# Manejo de errores
def t_error(t):
    print(f"Carácter incorrecto '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

# Aqui contruimos el lexer
lexer = lex.lex()

def test_lexer(data):  
    lexer.input(data)
    print(f"Revisando el input: {data}")
    tokens_found = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Token: {tok.type} - Valor: {repr(tok.value)} - Línea actual : {tok.lineno}")
        tokens_found.append((tok.type, tok.value))
    
    return tokens_found

 ##! CASOS DE PRUEBA NO CUENTA PARA el PROYECTO  (SE DEBE ELIMINAR ESTO PARA EL FINAL Y SOLO PROBAR CON NUESTROS ALGORITMOS)

if __name__ == "__main__":
    print("=== ANALIZADOR LEXICO KOTLIN-LIKE ===\n")

    # Caso 1: Declaración de variables
    print("🧪 CASO 1: Declaracion de variables")
    test_code1 = '''val nombre: String = "Cristhian"
var edad: Int = 25
var precio: Double = 19.99'''
    test_lexer(test_code1)
    print()
    
    
    # Caso 3: Función simple
    print("🧪 CASO 3: Función simple")
    test_code3 = '''fun saludar(nombre: String): String {
    return "Hola " + nombre
}'''
    test_lexer(test_code3)
    print()
    
    # Caso 5: Null safety
    print("🧪 CASO 5: Null safety")
    test_code5 = '''val nombre: String? = "Juan"
val longitud = nombre?.length ?: 0'''
    test_lexer(test_code5)
    print()
    
    # Caso 6: Estructura when
    print("🧪 CASO 6: Estructura when")
    test_code6 = '''when (edad) {
    18 -> println("Adulto joven")
    65 -> println("Adulto mayor")
}'''
    test_lexer(test_code6)
    print()
    
