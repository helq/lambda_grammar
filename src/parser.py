#-*- coding: utf-8 -*-
# module: parser.py
# author: helq
# license: wtfpl
# This module just grammatical rules

from src.tokrules import tokens

precedence = (
    # it's not an operator
    ('nonassoc', 'DOT'), # no matter if it's nonassoc, right or left

    # real operators
    ('right', 'CONS'),
    ('right', 'CONCAT'),
    ('left', 'AND', 'OR'),
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN', 'EQUAL', 'DIFF_OP'),  # Nonassociative operators
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),

    # they aren't operators
    ('nonassoc', 'APPL'), # no matter if it's nonassoc, right or left
    ('nonassoc', 'ID'), # no matter if it's nonassoc, right or left
)

def p_S(p):
    'S : S declaration'
    toRet = p[1]
    id, λ_term = p[2]
    toRet[id] = λ_term
    p[0] = toRet
def p_S2(p):
    'S : '
    p[0] = {}

def p_declaration(p):
    'declaration : ID EQUAL lambda_term DOT'
    p[0] = p[1], p[3]


# λ_term
def p_λ_term1(p):
    '''lambda_term : abstraction
                   | application %prec APPL
                   | value'''
    p[0] = p[1]

def p_λ_term2(p):
    'lambda_term : ID %prec APPL'
    p[0] = {'type': 'id', 'id': p[1]}

def p_λ_term3(p):
    '''lambda_term : lambda_term CONS        lambda_term
                   | lambda_term CONCAT      lambda_term
                   | lambda_term PLUS        lambda_term
                   | lambda_term MINUS       lambda_term
                   | lambda_term TIMES       lambda_term
                   | lambda_term DIVIDE      lambda_term
                   | lambda_term LESSTHAN    lambda_term
                   | lambda_term GREATERTHAN lambda_term
                   | lambda_term EQUAL       lambda_term
                   | lambda_term DIFF_OP     lambda_term
                   | lambda_term AND         lambda_term
                   | lambda_term OR          lambda_term'''
    p[0] = {'type': 'op', 'op': p[2], 'val1': p[1], 'val2': p[3]}

def p_λ_term_enclosed(p):
    'lambda_term : LPAREN lambda_term RPAREN %prec APPL'
    p[0] = p[2]

# λ_abstraction
def p_λ_abstraction(p):
    'abstraction : LAMBDA ID DOT lambda_term'
    p[0] = {'type': 'λ_abstraction', 'param': p[2], 'λ_term': p[4]}

# λ_application
def p_λ_application(p):
    'application : application ID'
    tmp = p[1]
    tmp['input'].append( {'type': 'id', 'id': p[2]} )
    p[0] = tmp
def p_λ_application3(p):
    'application : application value'
    tmp = p[1]
    tmp['input'].append( p[2] )
    p[0] = tmp
def p_λ_application2(p):
    'application : application LPAREN lambda_term RPAREN'
    tmp = p[1]
    tmp['input'].append( p[3] )
    p[0] = tmp

def p_λ_application_single(p):
    'application : ID ID'
    p[0] = { 'type': 'λ_application'
           , 'function': {'type': 'id', 'id': p[1]}
           , 'input': [{'type': 'id', 'id': p[2]}]}
def p_λ_application_single8(p):
    'application : ID value'
    p[0] = { 'type': 'λ_application'
           , 'function': {'type': 'id', 'id': p[1]}
           , 'input': [p[2]]}
def p_λ_application_single2(p):
    'application : ID LPAREN lambda_term RPAREN'
    p[0] = { 'type': 'λ_application'
           , 'function': {'type': 'id', 'id': p[1]}
           , 'input': [p[3]]}
def p_λ_application_single3(p):
    'application : LPAREN lambda_term RPAREN ID'
    p[0] = { 'type': 'λ_application'
           , 'function': p[2]
           , 'input': [{'type': 'id', 'id': p[4]}]}
def p_λ_application_single5(p):
    'application : LPAREN lambda_term RPAREN value'
    p[0] = { 'type': 'λ_application'
           , 'function': p[2]
           , 'input': [p[4]]}
def p_λ_application_single4(p):
    'application : LPAREN lambda_term RPAREN LPAREN lambda_term RPAREN'
    p[0] = {'type': 'λ_application', 'function': p[2], 'input': [p[5]]}

# λ_value
def p_value(p):
    '''value : STRING
             | TRUE
             | FALSE
             | NUMBER
             | NIL'''
    p[0] = {'type': 'value', 'value': p[1]}

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)
