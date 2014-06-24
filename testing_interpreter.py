#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import ply.lex as lex
import src.tokrules

import ply.yacc as yacc
from src.parser import *

import src.interpreter as inter

from src.repr import λ_term_to_str

lexer = lex.lex(module=src.tokrules)
parser = yacc.yacc()


def nothing(x): pass

if __name__ == "__main__":
    from sys import argv, setrecursionlimit
    setrecursionlimit(1000)
    if len(argv) != 2:
        print("how to use:\n "+argv[0]+" file_to_execute")
        exit(1)

    prelude = open('prelude.code', 'r').read()
    filecode = open(argv[1], 'r').read()
    declarations = parser.parse(prelude +" "+ filecode)

    if not 'main' in declarations:
        print("must be an 'main' simbol/declaration in the source code")
        exit(1)

    print( λ_term_to_str(declarations['main']), end="\n\n" )
    result = inter.reduce_λ_term(declarations['main'], declarations, print)
    print( "\n= " + λ_term_to_str(result) )
