import ply.lex as lex

tokens = [
    'true',
    'false',
    'null',
    'string',
    'number'
]

def t_null(t):
    r'null'
    return t
    
def t_true(t):
    r'true'
    return t

def t_false(t):
    r'false'
    return t

# los literales son chars que matchean de una
literals = "(){}[]:,"
#tokens = list(reserved.values()) + tokens

def t_string(t):
    # el primer ^ toma complemento de los símbolos que siguen
    #r'"([^"\n]|(\\"))*"$'
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    #r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
    #r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_number(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
