import ply.lex as lex

reserved = {
    'NULL' : 'NULL',
    'null' : 'NULL',
    'true' : 'TRUE',
    'TRUE' : 'TRUE',
    'FALSE': 'FALSE',
    'false': 'FALSE'
}

tokens = ['STRING','NUMBER'] + list(set(reserved.values()))


# los literales son chars que matchean de una
literals = "(){}[]:,"

def t_STRING(t):
    # We assume that t is a STRING and contains a '-' iif it surrounded by double quotes (")
    r'"[^"]*"|[a-zA-Z][a-zA-Z0-9\\]*'
    t.type = reserved.get(t.value,'STRING')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?((e|E)(\+|-)?\d*)?'
    # one o more digits possible follow by decimals and/or scientific denotation (e or E +/-) 
    return t

# This is only to print a better error message
def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)

t_ignore_WHITESPACES = r"[ \t]+"

def t_error(token):
    error_message = "Illegal Token"
    error_message += "\nvalue: {}".format(str(token.value[0]))
    error_message += "\nline:  {}".format(str(token.lineno))
    error_message += "\nposition:  {}".format(str(token.lexpos))
    print(error_message)
    token.lexer.skip(1)
    # An exception could also be thrown
    # raise Exception(error_message)
