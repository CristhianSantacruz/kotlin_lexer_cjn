import ply.yacc as yacc  
from kotlin_lexer import tokens  
from datetime import datetime
from pprint import pprint
import os
from pprint import pformat

# Precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'UMINUS'),
)


context_semantico = {
    'en_funcion': False,
    'en_bucle': False,
    'nivel_bucle': 0,
    'funciones_definidas': set(),
    'variables_definidas': set(),
    'tipos_variables': {},
    'parametros_funcion_actual': [],
    'tipo_retorno_funcion_actual': None
}

errors_semanticos = []


def reset_context_semantico():
    global context_semantico, errors_semanticos
    context_semantico = {
        'en_funcion': False,
        'en_bucle': False,
        'nivel_bucle': 0,
        'funciones_definidas': set(),
        'variables_definidas': set(),
        'tipos_variables': {},
        'parametros_funcion_actual': [],
        'tipo_retorno_funcion_actual': None
    }
    errors_semanticos = []
    return

def add_error_semantico(mensaje, lineno=None):
    """Agrega un error semántico a la lista"""
    if lineno:
        error_msg = f"Error semántico en línea {lineno}: {mensaje}"
    else:
        error_msg = f"Error semántico: {mensaje}"
    errors_semanticos.append(error_msg)
    print(error_msg)

def get_lineno(p, index=1):
    """Obtiene el número de línea del token en la posición dada"""
    try:
        return p.lineno(index)
    except:
        return None


# Reglas sintácticas generales
def p_program(p):
    """program : statement_list"""
    p[0] = p[1]

def p_statement_list_multiple(p):
    """statement_list : statement_list statement"""
    p[1].append(p[2])
    p[0] = p[1]

def p_statement_list_single(p):
    """statement_list : statement"""
    p[0] = [p[1]]

def p_statement_list_empty(p):
    """statement_list : """
    p[0] = []

def p_statement(p):
    '''statement : declaration
                 | function_def
                 | function_def_params_no_return
                 | function_def_no_params_no_return
                 | function_def_no_params_with_return
                 | class_def
                 | for_loop
                 | when_stmt
                 | print_stmt
                 | return_stmt
                 | break_stmt
                 | continue_stmt
                 | if_else
                 | expression_stmt'''
    p[0] = p[1]






# Comienza Jahir Díaz Cedeño
#___________________________

# Declaración de variables (val/var)
def p_declaration(p):
    '''declaration : VAR ID ASSIGN expression
                   | VAL ID ASSIGN expression'''
    p[0] = ("declare", p[1], p[2], p[4])
    #------Noelia Saltos, prueba de la regla semantica---------
    context_semantico['variables_definidas'].add(p[2])
    #------Noelia Saltos, Fin prueba de la regla semantica---------

# Función con valor de retorno
def p_function_def(p):
    """function_def : FUN ID LPAREN param_list_opt RPAREN COLON type block"""
    #------Jahir Díaz, prueba de la regla semantica---------
    context_semantico['tipo_retorno_funcion_actual'] = p[7]
    context_semantico['en_funcion'] = True
    context_semantico['funciones_definidas'].add(p[2])
    verificar_tipo_retorno_funcion(p)  # <- Validación semántica
    context_semantico['en_funcion'] = False
    #------Jahir Díaz, prueba de la regla semantica---------
    p[0] = ("func_def", p[2], p[4], p[7], p[8])

def p_param_list_opt(p):
    '''param_list_opt : param_list
                      | '''
    p[0] = p[1] if len(p) > 1 else []

def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

def p_param(p):
    """param : ID COLON type"""
    p[0] = (p[1], p[3])

def p_type(p):
    """type : TYPE_INT
            | TYPE_DOUBLE
            | TYPE_BOOLEAN
            | TYPE_STRING
            | ID"""
    p[0] = p[1]

# Return
def p_return_stmt(p):
    """return_stmt : RETURN expression"""
    p[0] = ("return", p[2])

# Estructura de control: bucle for
def p_for_loop(p):
    """for_loop : FOR LPAREN ID IN expression RPAREN loop_body"""
    p[0] = ("for", p[3], p[5], p[7])

def p_loop_body(p):
    '''loop_body : block
                 | statement'''
    p[0] = p[1] if isinstance(p[1], list) else [p[1]]

# Estructura de datos: mapOf
def p_expression_map(p):
    """expression : MAPOF LPAREN map_entries RPAREN"""
    p[0] = ("map", p[3])

def p_map_entries_multiple(p):
    """map_entries : map_entries COMMA map_entry"""
    p[1].append(p[3]); p[0] = p[1]

def p_map_entries_single(p):
    """map_entries : map_entry"""
    p[0] = [p[1]]

def p_map_entry(p):
    """map_entry : expression TO expression"""
    p[0] = (p[1], p[3])

# Expresiones

def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression LESS expression
                  | expression GREATER expression
                  | expression LESS_EQUAL expression
                  | expression GREATER_EQUAL expression
                  | expression EQUALS expression
                  | expression NOT_EQUALS expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ("binop", p[2], p[1], p[3])
    # -- Noelia Saltos, prueba de la regla semantica---------
    verificar_operacion_binaria_compatible(p[0])
    # -- Noelia Saltos, Fin prueba de la regla semantica---------


def p_expression_unary(p):
    """expression : MINUS expression %prec UMINUS"""
    p[0] = ("uminus", p[2])

def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]

def p_expression_literal(p):
    '''expression : NUMBER_INT
                  | NUMBER_DOUBLE
                  | STRING
                  | BOOLEAN_TRUE
                  | BOOLEAN_FALSE'''
    p[0] = ("literal", p[1])

def p_expression_id(p):
    """expression : ID"""
    p[0] = ("id", p[1])
    # -- Noelia Saltos, prueba de la regla semantica---------
    verificar_variables_declaradas(('use_var', p[1]))
    # ------------Fin Noelia Saltos

# Impresión
def p_print_stmt(p):
    """print_stmt : PRINTLN LPAREN expression RPAREN"""
    p[0] = ("print", p[3])

def p_print_stmt_print(p):
    """print_stmt : PRINT LPAREN expression RPAREN"""
    p[0] = ("print", p[3])

# Bloques de código
def p_block(p):
    """block : LBRACE statement_list RBRACE"""
    p[0] = p[2]

# Expresión como sentencia aislada
def p_expression_stmt(p):
    """expression_stmt : expression"""
    p[0] = ("expr_stmt", p[1])

# Termina Jahir Díaz Cedeño
#___________________________



# Comienzo Cristhian Santacruz

#Estructura listOf

def p_expression_listOf(p):
    """expression : LISTOF LPAREN expression_list RPAREN"""
    p[0] = ("listOf", p[3])


def p_expression_list_multiple(p):
    """expression_list : expression_list COMMA expression"""
    p[1].append(p[3])
    p[0] = p[1]

def p_expression_list_single(p):
    """expression_list : expression"""
    p[0] = [p[1]]

def p_expression_list_empty(p):
    """expression_list : """
    p[0] = []

#Estructura de control

def p_when_stmt(p):
    """when_stmt : WHEN LPAREN expression RPAREN LBRACE when_branches RBRACE"""
    p[0] = ("when_stmt", p[3], p[6])

def p_when_branches_multiple(p):
    """when_branches : when_branches when_branch"""
    p[1].append(p[2])
    p[0] = p[1]

def p_when_branches_single(p):
    """when_branches : when_branch"""
    p[0] = [p[1]]

def p_when_branch_expression(p):
    """when_branch : expression ARROW statement_list"""
    p[0] = ("when_case", p[1], p[3])

def p_when_branch_else(p):
    """when_branch : ELSE ARROW statement_list"""
    p[0] = ("when_else", p[3])


def p_when_stmt_without_expr(p):
    """when_stmt : WHEN LBRACE when_branches RBRACE"""
    p[0] = ("when_stmt_no_expr", p[3])

# Función sin retorno
def p_function_def_params_no_return(p):
    """function_def_params_no_return : FUN ID LPAREN param_list RPAREN block"""
    p[0] = ("func_def_params_no_return", p[2], p[4], p[6])





# Definician de clases , propiedades y metodos
def p_class_def(p):
    """class_def : CLASS ID LBRACE class_body RBRACE"""
    p[0] = ("class_def", p[2], p[4])

def p_class_body_multiple(p):
    """class_body : class_body class_member"""
    p[1].append(p[2])
    p[0] = p[1]

def p_class_body_single(p):
    """class_body : class_member"""
    p[0] = [p[1]]

def p_class_body_empty(p):
    """class_body : """
    p[0] = []

def p_class_member(p):
    '''class_member : property_def
                    | method_def'''
    p[0] = p[1]

def p_property_def(p):
    '''property_def : VAR ID COLON type
                    | VAL ID COLON type
                    | VAR ID COLON type ASSIGN expression
                    | VAL ID COLON type ASSIGN expression'''
    if len(p) == 5:
        p[0] = ("property", p[1], p[2], p[4], None)
    else:
        p[0] = ("property", p[1], p[2], p[4], p[6])
        #------Jahir Díaz, prueba de la regla semantica---------
        verificar_asignacion_tipada(p)
        #------Jahir Díaz, prueba de la regla semantica---------

def p_method_def(p):
    """method_def : FUN ID LPAREN param_list_opt RPAREN block"""
    p[0] = ("method", p[2], p[4], p[6])

# Termina Cristhian Santacruz

#TERCER AVANCE, CON FECHA DE ENTREGA DEL 29/06/2025

#Inicio Semantico Jahir Díaz Cedeño
# Verificación semántica de tipos

def inferir_tipo_expresion(expr):
    if isinstance(expr, tuple) and len(expr) > 1:
        if expr[0] == "literal":
            value = expr[1]
            if isinstance(value, bool):
                return "Boolean"
            elif isinstance(value, int):
                return "Int"
            elif isinstance(value, float):
                return "Double"
            elif isinstance(value, str):
                return "String"
    return "Unknown"

def verificar_asignacion_tipada(p):
    if len(p) == 7:
        tipo = p[4]  # tipo explícito
        expr = p[6]
        tipo_expr = inferir_tipo_expresion(expr)
        if tipo_expr != "Unknown" and tipo_expr != tipo:
            add_error_semantico(f"Tipo incompatible en la asignación. Esperado '{tipo}', pero se encontró '{tipo_expr}'", getattr(p, 'lineno', None))

        # Validación específica para Boolean (true/false solamente)
        if tipo == "Boolean" and tipo_expr != "Boolean":
            add_error_semantico(f"Tipo inválido para Boolean. Solo se permite true o false, se encontró '{tipo_expr}'", getattr(p, 'lineno', None))

#Se implementaron dos reglas semánticas para la validación de tipos en asignaciones.
#La primera regla verifica que el tipo declarado de una variable coincida con el tipo inferido de la expresión asignada, generando un error semántico si son incompatibles.
#La segunda regla añade una validación específica para variables del tipo Boolean, asegurando que únicamente acepten los valores true o false como asignación válida.

#Inicio Semantico Jahir Díaz Cedeño
def verificar_tipo_retorno_funcion(p):
    tipo_esperado = context_semantico['tipo_retorno_funcion_actual']
    if tipo_esperado is not None:
        valor = p[2]
        tipo_real = inferir_tipo_expresion(valor)
        if tipo_real != tipo_esperado:
            add_error_semantico(f"Tipo de retorno incorrecto. Se esperaba '{tipo_esperado}' pero se obtuvo '{tipo_real}'", getattr(p, 'lineno', None))

def validar_funcion_unit_sin_return(body):
    for sentencia in body:
        if isinstance(sentencia, tuple) and sentencia[0] == "return":
            add_error_semantico("Una función sin tipo de retorno no debe contener una instrucción return con valor.")
# La primera regla valida que el tipo de valor retornado en una función coincida con el tipo de retorno declarado.
# La segunda regla verifica que las funciones declaradas sin tipo de retorno (Unit) no contengan instrucciones return con valores, ya que esto violaría su definición.



#Fin Semantico Jahir Díaz Cedeño

#Fin Semantico Jahir Díaz Cedeño

#Inicio Semantico Noelia Saltos Hernandez

# 1era Regla .- Se valida que las operaciones entre variables o literales se realicen entre tipos compatibles.
# 2da Regla .- Y se verifica que las comparaciones lógicas se hagan entre tipos compatibles.

def verificar_operacion_binaria_compatible(expr):
    if expr[0] == "binop":
        _, op, izq, der = expr
        tipo_izq = inferir_tipo_expresion(izq)
        tipo_der = inferir_tipo_expresion(der)

        if op == '+':
            # Permitir Int + Int, Double + Double, Int + Double, String + String
            if (tipo_izq in ["Int", "Double"] and tipo_der in ["Int", "Double"]) or (tipo_izq == "String" and tipo_der == "String"):
                return
            else:
                add_error_semantico(f"Operación '+' incompatible entre '{tipo_izq}' y '{tipo_der}'")

        elif op in ['-', '*', '/']:
            if tipo_izq not in ["Int", "Double"] or tipo_der not in ["Int", "Double"]:
                add_error_semantico(f"Operación '{op}' incompatible entre '{tipo_izq}' y '{tipo_der}'")

        elif op in ['>', '<', '>=', '<=', '==', '!=']:
            if tipo_izq != tipo_der:
                add_error_semantico(f"Comparación entre tipos incompatibles: '{tipo_izq}' y '{tipo_der}'")

# 3era Regla .- Se verifica las variables no deben ser usadas antes de ser declaradas
def verificar_variables_declaradas(expr):
    if isinstance(expr, tuple):
        if expr[0] == 'var':
            varname = expr[1]
            context_semantico['variables_definidas'].add(varname)
        elif expr[0] == 'use_var':
            varname = expr[1]
            if varname not in context_semantico['variables_definidas']:
                add_error_semantico(f"La variable '{varname}' se está usando antes de ser declarada.")

 

#Fin Semantico Noelia Saltos Hernandez


#Semantico Cristhian Santacruz

def p_break_stmt(p):
    """break_stmt : BREAK"""
   
    p[0] = ("break",)

def p_continue_stmt(p):
    """continue_stmt : CONTINUE"""
    
    p[0] = ("continue",)

def p_function_def_no_params_with_return(p):
    """function_def_no_params_with_return : FUN ID LPAREN RPAREN COLON type block"""
    # Establecer contexto antes de procesar
    context_semantico['en_funcion'] = True
    context_semantico['funciones_definidas'].add(p[2])
    context_semantico['tipo_retorno_funcion_actual'] = p[6]
    
    # El bloque ya fue procesado por el parser con el contexto activo
    # Ahora restablecer el contexto después del procesamiento
    context_semantico['en_funcion'] = False
    context_semantico['tipo_retorno_funcion_actual'] = None
    p[0] = ("func_def_no_params_with_return", p[2], [], p[6], p[7])


def inferir_tipo_expresion(expr):
    """Función auxiliar para inferir tipos básicos de expresiones"""
    if isinstance(expr, tuple) and len(expr) > 1:
        if expr[0] == "literal":
            value = expr[1]
            if isinstance(value, bool):
                return "Boolean"
            elif isinstance(value, int):
                return "Int"
            elif isinstance(value, float):
                return "Double"
            elif isinstance(value, str):
                return "String"
    return "Unknown"

#Se agrego la función inferir_tipo_expresion para poder inferir el tipo de una expresión

# Se analizo tambien la semantica de la estructura de control if-else
def verificar_semantica_completa(ast):
    """Verificar todas las reglas semánticas después de construir el AST"""
    for nodo in ast:
        verificar_nodo_semantica(nodo, contexto_local={'en_funcion': False, 'en_bucle': False})

def verificar_nodo_semantica(nodo, contexto_local):
    """Verificar semántica de un nodo recursivamente"""
    if not isinstance(nodo, tuple):
        return
        
    tipo = nodo[0]

    print("ESTAMOS VERIFICANDO NODOS")
    
    if tipo in ['func_def', 'func_def_no_params_with_return', 'func_def_params_no_return', 'func_def_no_params_no_return']:
        # Estamos entrando a una función
        nuevo_contexto = contexto_local.copy()
        nuevo_contexto['en_funcion'] = True
        
        # Verificar el cuerpo de la función
        cuerpo = nodo[-1]  # El cuerpo suele ser el último elemento
        if isinstance(cuerpo, list):
            for stmt in cuerpo:
                verificar_nodo_semantica(stmt, nuevo_contexto)
                
    elif tipo == 'for':
        print("ESTAMOS DENTOR DE UN FOR")
        # Estamos entrando a un bucle for
        nuevo_contexto = contexto_local.copy()
        nuevo_contexto['en_bucle'] = True
        
        # Verificar el cuerpo del bucle (último elemento)
        cuerpo = nodo[-1]  # El cuerpo del for
        if isinstance(cuerpo, list):
            for stmt in cuerpo:
                verificar_nodo_semantica(stmt, nuevo_contexto)
        else:
            verificar_nodo_semantica(cuerpo, nuevo_contexto)
                
    elif tipo == 'return':
        if not contexto_local.get('en_funcion', False):
            add_error_semantico("'return' solo puede usarse dentro de una función")
            
    elif tipo == 'break':
        if not contexto_local.get('en_bucle', False):
            add_error_semantico("'break' solo puede usarse dentro de un bucle")
            
    elif tipo == 'continue':
        if not contexto_local.get('en_bucle', False):
            add_error_semantico("'continue' solo puede usarse dentro de un bucle")
            
    else:
        # Verificar recursivamente otros nodos
        for i in range(1, len(nodo)):
            child = nodo[i]
            if isinstance(child, (list, tuple)):
                if isinstance(child, list):
                    for item in child:
                        verificar_nodo_semantica(item, contexto_local)
                else:
                    verificar_nodo_semantica(child, contexto_local)



#Fin Semantico Cristhian Santacruz



# Comienza Noelia Saltos
def p_expression_arrayof(p):
    """expression : ARRAYOF LPAREN expression_list RPAREN"""
    p[0] = ("arrayOf", p[3])

def p_if_else(p):
    '''if_else : IF LPAREN expression RPAREN block ELSE block'''
    expr_tipo = inferir_tipo_expresion(p[3])
    if expr_tipo != "Unknown" and expr_tipo != "Boolean":
        add_error_semantico(f"La condición del if debe ser de tipo Boolean, se encontró '{expr_tipo}'", getattr(p, 'lineno', None))
    p[0] = ("if_else", p[3], p[5], p[7])

def p_function_def_no_params_no_return(p):
    """function_def_no_params_no_return : FUN ID LPAREN RPAREN block"""
    #------Jahir Díaz, prueba de la regla semantica---------
    validar_funcion_unit_sin_return(p[5])
    #------Jahir Díaz, prueba de la regla semantica---------
    p[0] = ("func_def_no_params_no_return", p[2], [], p[5])

def p_expression_readline(p):
    '''expression : READLINE LPAREN RPAREN'''
    p[0] = ("readLine",)


errores_sintacticos = [] 
# Manejo de errores y creación de logs
def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en token '{p.type}' (valor: {p.value}) en la línea {p.lineno}"
    else:
        error_msg = "Error de sintaxis: fin inesperado del archivo (EOF)"
    
    print(error_msg)
    errores_sintacticos.append(error_msg)

# Parser
parser = yacc.yacc()


#INTERPRETE
contexto = {}

def ejecutar_programa(arbol):
    contexto = {}
    for nodo in arbol:
        ejecutar_nodo(nodo, contexto)

def ejecutar_nodo(nodo, contexto):
    tipo = nodo[0]

    if tipo == "declare":
        _, modo, nombre, valor_expr = nodo
        valor = evaluar_expresion(valor_expr, contexto)
        contexto[nombre] = valor

    elif tipo == "print":
        _, expr = nodo
        valor = evaluar_expresion(expr, contexto)
        print(valor)

    elif tipo == "expr_stmt":
        evaluar_expresion(nodo[1], contexto)

    elif tipo == "func_def_no_params_no_return":
        # No ejecutamos funciones aún, pero podrías almacenarlas en contexto si lo deseas
        print(f"Función '{nodo[1]}' definida pero no ejecutada automáticamente.")


def evaluar_expresion(expr, contexto):
    if expr[0] == "literal":
        return expr[1]

    elif expr[0] == "id":
        nombre = expr[1]
        return contexto.get(nombre, f"<{nombre} no definido>")

    elif expr[0] == "readLine":
        return input(" Ingresa un valor: ")

    elif expr[0] == "binop":
        _, op, izq, der = expr
        val_izq = evaluar_expresion(izq, contexto)
        val_der = evaluar_expresion(der, contexto)

        # Convierte a float solo si ambos son numéricos
        try:
            val_izq = float(val_izq)
            val_der = float(val_der)
        except ValueError:
            pass  # Si no son números, se mantendrán como string para concatenar con +

        if op == "+":
            if isinstance(val_izq, str) or isinstance(val_der, str):
                return str(val_izq) + str(val_der)
            else:
                return val_izq + val_der
        elif op == "-":
            return val_izq - val_der
        elif op == "*":
            return val_izq * val_der
        elif op == "/":
            return val_izq / val_der

# Función para probar parser
# Función para analizar un archivo y guardar el log
def analizar_archivo_sintactico(nombre_archivo, usuario_git="usuarioGit"):
    global errores_sintacticos
    errores_sintacticos = []  # Limpiar antes de cada análisis

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        print(f"-Analizando archivo: {nombre_archivo}")
        resultado = parser.parse(contenido)
       

        
        now = datetime.now()
        timestamp = now.strftime("%d%m%Y-%Hh%M")
        log_filename = f"logs/sintactico-{usuario_git}-{timestamp}.txt"
        os.makedirs("logs", exist_ok=True)

        with open(log_filename, "w", encoding="utf-8") as f:
            f.write("=== LOG DE ANALISIS SINTACTICO ===\n")
            f.write(f"Usuario: {usuario_git}\n")
            f.write(f"Fecha y hora: {timestamp}\n")
            f.write(f"Archivo: {nombre_archivo}\n\n")
            f.write("Código fuente analizado:\n")
            f.write("-" * 40 + "\n")
            f.write(contenido + "\n")
            f.write("-" * 40 + "\n\n")
                   
            if errores_sintacticos:
                f.write(" ERRORES DE SINTAXIS:\n")
                for error in errores_sintacticos:
                    f.write(f"{error}\n")
            else:
                f.write("Sintaxis válida. Resultado del análisis:\n")
                f.write(pformat(resultado, indent=2, width=80))

        print("Log generado:", log_filename)

    except FileNotFoundError:
        print(f"Archivo '{nombre_archivo}' no encontrado.")



#Fin Noelia Saltos Hernandez


##Funcion para analizar un archivo y guardar el log 
def analizar_archivo_sintactico_semantico(nombre_archivo, usuario_git="usuarioGit"):
    global errores_sintacticos
    errores_sintacticos = []
    reset_context_semantico()  
   

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        print(f"-Analizando archivo: {nombre_archivo}")
        resultado = parser.parse(contenido)
        
        if resultado:
            print("ESTAMOS VERIFICANDO SEMANTICA COMPLETA")
            verificar_semantica_completa(resultado)
            if not errores_sintacticos:
                ejecutar_programa(resultado)
        
        if resultado and not errores_sintacticos and not errors_semanticos:
            ejecutar_programa(resultado)

        now = datetime.now()
        timestamp = now.strftime("%d%m%Y-%Hh%M")
        log_filename = f"logs/sintactico-semantico-{usuario_git}-{timestamp}.txt"
        os.makedirs("logs", exist_ok=True)

        with open(log_filename, "w", encoding="utf-8") as f:
            f.write("=== LOG DE ANALISIS SINTACTICO-SEMANTICO ===\n")
            f.write(f"Usuario: {usuario_git}\n")
            f.write(f"Fecha y hora: {timestamp}\n")
            f.write(f"Archivo: {nombre_archivo}\n\n")
            f.write("Código fuente analizado:\n")
            f.write("-" * 40 + "\n")
            f.write(contenido + "\n")
            f.write("-" * 40 + "\n\n")
            
            # Errores sintácticos
            if errores_sintacticos:
                f.write("❌ ERRORES DE SINTAXIS:\n")
                for error in errores_sintacticos:
                    f.write(f"  {error}\n")
                f.write("\n")
            else:
                f.write("✅ Análisis sintáctico exitoso\n\n")
            
            # Errores semánticos
            if errors_semanticos:
                f.write("❌ ERRORES SEMÁNTICOS:\n")
                for error in errors_semanticos:
                    f.write(f"  {error}\n")
                f.write("\n")
            else:
                f.write("✅ Análisis semántico exitoso\n\n")
            
            # Información del contexto semántico
            f.write("=== INFORMACIÓN SEMÁNTICA ===\n")
            f.write(f"Funciones definidas: {list(context_semantico['funciones_definidas'])}\n")
            f.write(f"Variables definidas: {list(context_semantico['variables_definidas'])}\n")
            f.write(f"Tipos de variables: {context_semantico['tipos_variables']}\n\n")
            
            # Resultado del análisis sintáctico
            if resultado and not errores_sintacticos:
                f.write("=== ARBOL SINTACTICO ===\n")
                f.write(pformat(resultado, indent=2, width=80))
                f.write("\n")

        print("Log generado:", log_filename)

    except FileNotFoundError:
        print(f"Archivo '{nombre_archivo}' no encontrado.")


#analizar_archivo_sintactico("algoritmo_sintactico1.kt", usuario_git="JDC1907")
#analizar_archivo_sintactico("algoritmo_sintactico2.kt", usuario_git="NoeSaltos")
#analizar_archivo_sintactico("algoritmo_sintactico3.kt", usuario_git="CristhianSantacruz")
analizar_archivo_sintactico_semantico("algoritmo_semantico3.kt", usuario_git="CristhianSantacruz")
analizar_archivo_sintactico_semantico("algoritmo_semantico1.kt", usuario_git="JDC1907")
analizar_archivo_sintactico_semantico("algoritmo_semantico2.kt", usuario_git="NoeSaltos")