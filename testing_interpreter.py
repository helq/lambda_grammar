#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import ply.lex as lex
import src.tokrules

import ply.yacc as yacc
from src.parser import *

import src.interpreter as inter

from src.repr import λ_term_to_str

def nothing(x): pass

help_message = """how to use:
 testing_interpreter.py [-v|(-p|-n)] -f file_to_execute

   -v   call by value (by default is the strategy `call by name`)
   -p   print each reduction (default)
   -n   not print reductions and print last result
                (this must be string, or it will fail) (override `-p`)

 examples:
    testing_interpreter.py -f examples/factorial.lambda
    testing_interpreter.py -nf examples/factorial.lambda
    testing_interpreter.py -vnf examples/beer.lambda
"""

lexer = lex.lex(module=src.tokrules)
parser = yacc.yacc()

if __name__ == "__main__":
    import argv, sys
    #sys.setrecursionlimit(40)

    arguments = argv.parse(sys.argv)

    if 'f' not in arguments:
        print(help_message)
        exit(1)

    myPrint = nothing if 'n' in arguments else print

    prelude = open('prelude.code', 'r').read()
    filecode = open(arguments['f'], 'r').read()
    declarations = parser.parse(prelude +" "+ filecode)

    if not 'main' in declarations:
        print("must be an 'main' simbol/declaration in the source code")
        exit(1)

    # printing
    if 'n' not in arguments:
        print( λ_term_to_str(declarations['main']), end="\n\n" )

    inter.call_by_value_substitution = 'v' in arguments
    result = inter.reduce_λ_term(declarations['main'], declarations, myPrint)

    if 'n' in arguments:
        print( eval(λ_term_to_str(result)) )
    else:
        print( "\n= " + λ_term_to_str(result) )
