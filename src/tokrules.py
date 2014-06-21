#-*- coding: utf-8 -*-
# module: tokrules.py
# author: helq
# license: wtfpl
# This module just contains the lexing rules

reserved = {
   'true' : 'TRUE',
   'false' : 'FALSE',
   'nil'  : 'NIL',
}

tokens = [
   'STRING', 'NUMBER',
   'ID', 'LAMBDA',
   'LPAREN', 'RPAREN', 'DOT', 'EQUAL',
# operators
   'CONS', 'CONCAT',
   'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
   'DIFF_OP',
   'LESSTHAN', 'GREATERTHAN', 'AND', 'OR',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_DOT         = r'\.'
t_EQUAL       = r'='
t_CONS        = r':'

t_CONCAT      = r'\^'
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_LESSTHAN    = r'<'
t_GREATERTHAN = r'>'
t_AND         = r'&'
t_OR          = r'\|'
t_LAMBDA      = r'\\|λ'

def t_ID(t):
    r"[a-zA-Z][a-zA-Z_0-9]*'*"
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    if t.value == "true":  t.value = True
    if t.value == "false": t.value = False
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
    t.value = eval(t.value)
    return t

def t_DIFF_OP(t):
    r'/=|≠'
    t.value = '≠'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# a comment
def t_ignore_comments(t):
    r'\\\\[^\n]*'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)
