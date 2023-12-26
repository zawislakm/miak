import sys

import ply.lex as lex
import ply.yacc as yacc

if len(sys.argv) == 2:
    input_filename = sys.argv[1]
else:
    input_filename = "input1.m"
output_filename = "output.cpp"

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    '==': 'COMPARISON',
    '<=': 'LESSEQUAL',
    '>=': 'GREATEREQUAL',
    'end': 'END',
    'disp': 'DISP',
    'while': 'WHILE',
    'mod': "MOD"
}

tokens = [
             'NUMBER', 'ID', 'STRING',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
             'GREATER', 'LESS',
             'SEMICOLON', 'COMMA', 'EQUALS', 'LPAREN', 'RPAREN', 'COLON', 'COMMENT',
         ] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COMPARISON = r'=='
t_EQUALS = r'\='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_IF = r'if'
t_COLON = r'\:'
t_DISP = r'\disp'
t_MOD = r'mod'
t_END = r"end"

DECLARED = set()


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_STRING(t):
    r'".*"'
    return t


def t_NUMBER(t):
    r'\d+\.?\d*'
    return t

def t_COMMENT(t):
    r'%.*'
    return  t


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


def p_expression_string(t):
    'expression : STRING'
    t[0] = t[1]


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
            | if_statement
            | loop_statement
            | COMMENT
            '''
    t[0] = t[1]
    if len(t) == 3:
        t[0] += ";"

    if t[1][0] == "%":
        t[0] = "//" + t[1][1:]


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


def p_while(t):
    '''loop_statement : WHILE expression body END'''

    t[0] = f'while({t[2]})' + " {\n"
    if t[3]:
        for l in t[3]:
            t[0] += "    " + l + "\n"
    t[0] += "}\n"


def p_for(t):
    '''loop_statement : FOR expression EQUALS expression COLON expression body END
                       | FOR expression EQUALS expression COLON expression COLON expression body END'''
    if len(t) == 9:
        t[0] = f'for(auto {t[2]} = {t[4]}; {t[2]} <= {t[6]}; {t[2]} ++)'
        t[0] += "{\n"
        for l in t[7]:
            t[0] += l
        t[0] += "}\n"
    elif len(t) == 11:
        t[0] = f'for(auto {t[2]} = {t[4]}; {t[2]} <= {t[8]}; {t[2]} += {t[6]})'
        t[0] += "{\n"
        for l in t[9]:
            t[0] += l
        t[0] += "}\n"


def p_assign(t):
    '''statement : ID EQUALS expression'''
    global DECLARED
    if t[1] not in DECLARED:
        t[0] = f'auto {t[1]} = {str(t[3])}'
        DECLARED.add(t[1])
    else:
        t[0] = f'{t[1]} = {str(t[3])}'


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = "(" + t[2] + ")"


def p_compare_operator(t):
    '''compare_operator : COMPARISON
                    |  GREATER
                    |  LESS
                    |  LESSEQUAL
                    |  GREATEREQUAL'''
    t[0] = t[1]


def p_compare_expression(t):
    '''expression : expression compare_operator expression'''

    t[0] = f"{t[1]} {t[2]} {t[3]}"


def p_math_operator(t):
    '''math_operator : PLUS
                      | MINUS
                      | TIMES
                      | DIVIDE'''
    t[0] = t[1]


def p_expression_binop(t):
    '''expression : expression math_operator expression'''
    t[0] = f'{t[1]} {t[2]} {t[3]}'


def p_disp(t):
    ''' expression : DISP LPAREN expression RPAREN
                    | DISP LPAREN STRING RPAREN'''

    if len(t) == 5:
        t[0] = "cout<<"
        for x in t[3]:
            t[0] += str(x)
        t[0] += "<<endl"


def p_mod(t):
    '''expression : MOD LPAREN expression COMMA expression RPAREN'''
    t[0] = f'{t[3]} % {t[5]}'


parser = yacc.yacc()

f = open(input_filename, "rt")
lines = f.read()
parser.parse(lines)
f.close()

output_f.close()
