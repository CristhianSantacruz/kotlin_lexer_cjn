import ply.yacc as yacc  
from kotlin_lexer import tokens  
from datetime import datetime
import os


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
                 | function_def_no_return
                 | class_def
                 | for_loop
                 | when_stmt
                 | print_stmt
                 | return_stmt
                 | expression_stmt'''
    p[0] = p[1]





# Comienza Jahir Díaz Cedeño
#___________________________

# Declaración de variables (val/var)
def p_declaration(p):
    '''declaration : VAR ID ASSIGN expression
                   | VAL ID ASSIGN expression'''
    p[0] = ("declare", p[1], p[2], p[4])

# Función con valor de retorno
def p_function_def(p):
    """function_def : FUN ID LPAREN param_list_opt RPAREN COLON type block"""
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
def p_function_def_no_return(p):
    """function_def_no_return : FUN ID LPAREN param_list_opt RPAREN block"""
    p[0] = ("func_def_no_return", p[2], p[4], p[6])





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

def p_method_def(p):
    """method_def : FUN ID LPAREN param_list_opt RPAREN block"""
    p[0] = ("method", p[2], p[4], p[6])

# Termina Cristhian Santacruz



# Manejo de errores y creación de logs
def p_error(p):
    if p:
        error_msg = f"Syntax error at token {p.type} (value: {p.value})\n"
    else:
        error_msg = "Syntax error at EOF\n"

    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_filename = f"logs/sintactico-error-{timestamp}.txt"
    os.makedirs("logs", exist_ok=True)
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write(error_msg)

# Parser
parser = yacc.yacc()

# Función para probar parser
def test_parser(data, usuario_git="usuarioGit"):
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")
    filename = f"logs/sintactico-{usuario_git}-{timestamp}.txt"
    
    os.makedirs("logs", exist_ok=True)
    
    try:
        result = parser.parse(data)
        
        with open(filename, "w", encoding="utf-8") as log_file:
            log_file.write("=== LOG DE ANALISIS SINTACTICO ===\n")
            log_file.write(f"Usuario: {usuario_git}\n")
            log_file.write(f"Fecha y hora: {timestamp}\n\n")
            log_file.write("Código analizado:\n")
            log_file.write("-" * 40 + "\n")
            log_file.write(data + "\n")
            log_file.write("-" * 40 + "\n\n")
            
            if result:
                log_file.write("Resultado del análisis sintáctico:\n")
                log_file.write("ÉXITO - Código sintácticamente correcto\n\n")
                log_file.write("Árbol sintáctico generado:\n")
                for i, stmt in enumerate(result, 1):
                    stmt_info = f"Declaración {i}: {stmt}"
                    print(stmt_info)
                    log_file.write(stmt_info + "\n")
            else:
                error_msg = "ERROR - No se pudo generar el árbol sintáctico"
                print(error_msg)
                log_file.write(error_msg + "\n")
            
            log_file.write("\nFin del análisis sintáctico.\n")
            log_file.write("================================\n")
        
        print(f"\nResultado del análisis sintáctico guardado en: {filename}")
        return result
        
    except Exception as e:
        error_msg = f"Error durante el parsing: {e}"
        print(error_msg)
        
        with open(filename, "w", encoding="utf-8") as log_file:
            log_file.write("=== LOG DE ANALISIS SINTACTICO ===\n")
            log_file.write(f"Usuario: {usuario_git}\n")
            log_file.write(f"Fecha y hora: {timestamp}\n\n")
            log_file.write("Código analizado:\n")
            log_file.write("-" * 40 + "\n")
            log_file.write(data + "\n")
            log_file.write("-" * 40 + "\n\n")
            log_file.write("ERROR EN EL ANÁLISIS SINTÁCTICO:\n")
            log_file.write(str(e) + "\n")
            log_file.write("\nFin del análisis sintáctico.\n")
            log_file.write("================================\n")
        
        return None


