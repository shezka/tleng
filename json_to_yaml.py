#!/usr/bin/python3
import sys
from ply.lex import lex
from ply.yacc import yacc

import tokrules
import parser_rules

def read():
    # build athe json in a string 
    json = ""
    
    for line in sys.stdin:
        json += line

    return json

if __name__ == "__main__":
    try:
        expr = read()

        lexer = lex(module=tokrules)
        parser = yacc(module=parser_rules)
        
        ast = parser.parse(expr, lexer)
        print(ast.yaml())
    except Exception as e:
        print(e.__class__.__name__+": "+str(e))