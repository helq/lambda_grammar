#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import src.tokrules
import ply.lex as lex

lexer = lex.lex(module=src.tokrules)

def test(s):
    print("test for:\n   " + repr(i))
    lexer.input(s)
    for tok in lexer:
        print("    | "+ str(tok))

tests = [
    "3 + 4",
    "λx.x*2",
    r"\x.x+6",
    "main = (\\x.x*x)7:nil",
    "x = 'hi' : ' another string'",
]

for i in tests:
    test(i)
    print()
