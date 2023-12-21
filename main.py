import ply.lex as lex
import ply.yacc as yacc

input_filename = "input.m"
output_filename = "output.cpp"

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'int': 'INT',
    'return': 'RETURN',
    '==': 'COMPARISON',
    '++': 'INCREMENT',
    '--': 'DECREMENT',
    '<=': 'LESSEQUAL',
    '>=': 'GREATEREQUAL',
    'end': 'END',
    'break': "BREAK",
    'disp': 'DISP',
}

tokens = [
             'NUMBER', 'ID', 'STRING',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
             'GREATER', 'LESS', 'MODULO'
             , 'LBRACKET', 'RBRACKET',
             'SEMICOLON', 'COMMA', 'COLON', 'EQUALS', 'LPAREN', 'RPAREN'
         ] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'\='
t_COMPARISON = r'=='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_MODULO = r'mod'
t_IF = r'if'
t_RETURN = r'return'
t_COLON = r';'
t_DISP = r'\disp'
t_END = "end"


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    print(t.type)
    return t


def t_STRING(t):
    r'".*"'
    return t


def t_NUMBER(t):
    r'\d+\.?\d*'
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
output_f = open(output_filename, "wt")


def p_program(t):
    '''program : body
            | empty'''

    output = ("#include <iostream> \n "
              "using namespace std;\n"
              "int main() {\n")

    if t[1] is not None:
        for line in t[1]:
            output += line + "\n"

    output += ("return 0; "
               "}")
    output_f.write(output + "\n")


def p_expression_number(t):
    'expression : NUMBER'
    t[0] = str(t[1])


def p_expression_id(t):
    'expression : ID'
    t[0] = t[1]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = "(" + t[2] + ")"


def p_body(t):
    '''body : line body
            | empty'''
    if len(t) == 3:
        if t[2] is not None:
            t[0] = [t[1]] + t[2]
        else:
            t[0] = [t[1]]
    elif t[1] is not None:
        t[0] = [t[1]]


def p_empty(t):
    'empty :'


def p_line(t):
    '''line : statement SEMICOLON
            | expression SEMICOLON
            | if_statement'''
    # | loop_statement
    # '''
    t[0] = t[1]
    if len(t) == 3:
        t[0] += ";"


def p_ifstatement(t):
    '''if_statement : IF expression body END
                    | IF expression body ELSE body END'''


    if len(t) == 5:
        t[0] = "if( " + t[2] + "){\n"

        for l in t[3]:
            t[0] += l + "\n"

        t[0] += "}\n"
    else:
        t[0] = "if( " + t[2] + "){\n"

        for l in t[3]:
            t[0] += l + "\n"

        t[0] += "}else{\n"
        for l in t[5]:
            t[0] += l + "\n"
        t[0] += "}\n"


# def p_declaration(t):
#     'declaration :  ID'
#     t[0] = f'auto {t[1]} = {str(t[3])};'


def p_assign(t):
    '''statement : ID EQUALS expression'''
    # | declaration EQUALS expression'''
    t[0] = f'auto {t[1]} = {str(t[3])}'


def p_return_statement(t):
    '''statement : RETURN expression
                | RETURN'''
    if len(t) == 3:
        t[0] = "return " + str(t[2])
    else:
        t[0] = "return"


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = "(" + t[2] + ")"


def p_function_args(t):
    '''function_args : expression COMMA function_args
                    | expression
                    | empty
    '''

    if len(t) == 4:
        t[0] = [t[1]] + t[3]
    elif t[1] is not None:
        t[0] = [t[1]]
    else:
        t[0] = []


def p_disp(t):
    ''' expression : DISP LPAREN expression RPAREN'''
    #DISP LPAREN STRING COMMA function_args RPAREN COLON

    if len(t) == 5:
        t[0] = "cout<<"
        for x in t[3]:
            t[0] += str(x)
        t[0] += "<<endl"


parser = yacc.yacc()

f = open(input_filename, "rt")
lines = f.read()
parser.parse(lines)
f.close()

output_f.close()
