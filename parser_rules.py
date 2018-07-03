import ply.yacc as yacc

from tokrules import tokens
from expressions import *

## All the productions of our gramar

def p_value_string(expression):
    '''value : STRING'''
    expression[0] = String(expression[1])

def p_value_number(expression):
    '''value : NUMBER'''
    expression[0] = SimpleValue(expression[1])

def p_value_true(expression):
    '''value : TRUE'''
    expression[0] = SimpleValue(expression[1])

def p_value_false(expression):
    '''value : FALSE'''
    expression[0] = SimpleValue(expression[1])

def p_value_null(expression):
    '''value : NULL'''
    expression[0] = SimpleValue('')

def p_value_object(expression):
    '''value : object'''
    expression[0] = expression[1].value()

def p_value_array(expression):
    '''value : array'''
    expression[0] = ComposeValue(expression[1])

def p_object_empty(expression):
    '''object : '{' '}' '''
    expression[0] = EmptyObject()

def p_object_members(expression):
    '''object : '{' members '}' '''
    expression[0] = Object(expression[2])

def p_members_pair(expression):
    '''members : pair'''
    expression[0] = Member(expression[1])

def p_members_pairs(expression):
    '''members : pair ',' members'''
    expression[0] = Member(expression[1])
    expression[0].concat_member(expression[3])

def p_pair(expression):
    '''pair : STRING ':' value'''
    expression[0] = Pair(String(expression[1]), expression[3])

def p_array_empty(expression):
    '''array : '[' ']' '''
    expression[0] = EmptyArray()

def p_array_elements(expression):
    '''array : '[' elements ']' '''
    expression[0] = Array(expression[2])

def p_elements_value(expression):
    '''elements : value '''
    expression[0] = Element(expression[1])

def p_elements_elements(expression):
    '''elements : value ',' elements'''
    expression[0] = Element(expression[1])
    expression[0].concat_element(expression[3])
    
def p_error(subexpr):
    # In case no production matches
    raise Exception("Syntax error.")