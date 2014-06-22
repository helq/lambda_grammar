#-*- coding: utf-8 -*-
# module: interpreter.py
# author: helq
# license: wtfpl

primitives = ['if']

def reduce_λ_term(λ_term, declarations, myPrint=print):
    from src.repr import λ_term_to_str

    while(True):
        if λ_term['type'] in ['value', 'λ_abstraction']:
            return λ_term

        myPrint( "= " + λ_term_to_str(λ_term) )

        if λ_term['type'] == 'id':
            λ_term = declarations[ λ_term['id'] ]
            continue

        if λ_term['type'] == 'op':
            op = λ_term['op']

            newMyPrint = lambda x: myPrint("  |"+x)

            if λ_term['val1']['type'] == 'value':
                value1 = λ_term['val1']
            else:
                myPrint( "  l-> " + λ_term_to_str(λ_term['val1']) )
                value1 = reduce_λ_term(λ_term['val1'], declarations, newMyPrint )
                myPrint( "  |= " + λ_term_to_str(value1) )

            if λ_term['val2']['type'] == 'value':
                value2 = λ_term['val2']
            else:
                myPrint( "  r-> " + λ_term_to_str(λ_term['val2']) )
                value2 = reduce_λ_term(λ_term['val2'], declarations, newMyPrint )
                myPrint( "  |= " + λ_term_to_str(value2) )

            λ_term = {'type': 'value'}

            val1 = value1['value']
            val2 = value2['value']
            if op == ':': λ_term['value'] = (val1, val2)

            if op == '^':
                if type(val1) is not str or type(val2) is not str:
                    raise Exception("operator ^ only valid for strings")
                λ_term['value'] = val1 + val2

            if op in ['+', '-', '*', '/', '<', '>']:
                if type(val1) is not int or type(val2) is not int:
                    raise Exception("operator "+op+" only valid for numbers")
                if op == '+': λ_term['value'] = val1 + val2
                if op == '-': λ_term['value'] = val1 - val2
                if op == '*': λ_term['value'] = val1 * val2
                if op == '/': λ_term['value'] = val1 // val2
                if op == '<': λ_term['value'] = val1 < val2
                if op == '>': λ_term['value'] = val1 > val2

            if op in ['=', '≠']:
                if type(val1) != type(val2):
                    raise Exception("operator "+op+" need same type for the two expresions")
                if op == '=': λ_term['value'] = val1 == val2
                if op == '≠': λ_term['value'] = val1 != val2

            if op in ['&', '|']:
                if type(val1) is not bool or type(val2) is not bool:
                    raise Exception("operator "+op+" only valid for booleans")
                if op == '&': λ_term['value'] = val1 and val2
                if op == '|': λ_term['value'] = val1 or val2

            continue

        if λ_term['type'] == 'λ_application':
            if λ_term['function']['type'] in ["value", "op"]:
                return λ_term

            if λ_term['function']['type'] == "id":
                id = λ_term['function']['id']
                if id in primitives:
                    λ_term = evaluate_primitive(id, λ_term['input'], declarations)
                else:
                    λ_term['function'] = declarations[ id ]
                continue

            if λ_term['function']['type'] == "λ_abstraction":
                param = λ_term['function']['param']
                term = λ_term['function']['λ_term']
                input_ = λ_term['input'][0]

                new_λ_term = substitution(param, input_) (term)

                if len(λ_term['input']) > 1:
                    λ_term = { 'type': 'λ_application'
                             , 'function': new_λ_term
                             , 'input': λ_term['input'][1:] }
                else:
                    λ_term = new_λ_term

                continue

            if λ_term['function']['type'] == "λ_application":
                λ_term = { 'type': 'λ_application'
                         , 'function': λ_term['function']['function']
                         , 'input': λ_term['function']['input']+λ_term['input']}
                continue

def substitution(x, N):
    def f(M):
        if M["type"] == 'value': return M
        if M["type"] == 'op':
            return { 'type': 'op'
                   , 'op': M['op']
                   , 'val1': f(M['val1'])
                   , 'val2': f(M['val2']) }

        if M["type"] == 'id':
            if M['id'] == x: return N
            else:            return M
        if M["type"] == 'λ_application':
            return { 'type': 'λ_application'
                   , 'function': f(M['function'])
                   , 'input': list(map(f, M['input'])) }
        if M["type"] == 'λ_abstraction':
            y = M['param']
            if y == x: return M
            else:
                if y in FV(N):
                    V_M_plus_V_N = V(M)
                    V_M_plus_V_N.update( V(N) )
                    newY = valNotIn( V_M_plus_V_N )

                    M = { 'type': 'λ_abstraction'
                        , 'param': newY
                        , 'λ_term': substitution(newY, N)(M['λ_term'])
                        }
                return { 'type': 'λ_abstraction'
                       , 'param': M['param']
                       , 'λ_term': f(M['λ_term'])
                       }
    return f

def FV(N):
    if N['type'] == 'value': return {}
    if N['type'] == 'op':
        FV_val1 = FV(N['val1'])
        FV_val2 = FV(N['val2'])
        FV_val1.update(FV_val2)
        return FV_val1

    if N['type'] == 'id':    return {N['id']: None}
    if N['type'] == 'λ_application':
        FV_function = FV(N['function'])
        FV_input = list(map(FV, N['input']))
        for i in FV_input:
            FV_function.update(i)
        return FV_function
    if N["type"] == 'λ_abstraction':
        FV_λ_term = FV(N['λ_term'])
        del( FV_λ_term[ N['param'] ] )
        return FV_λ_term

def V(N):
    if N['type'] == 'value': return {}
    if N['type'] == 'op':
        FV_val1 = FV(N['val1'])
        FV_val2 = FV(N['val2'])
        FV_val1.update(FV_val2)
        return FV_val1

    if N['type'] == 'id':    return {N['id']: None}
    if N['type'] == 'λ_application':
        FV_function = FV(N['function'])
        FV_input = list(map(FV, N['input']))
        for i in FV_input:
            FV_function.update(i)
        return FV_function
    if N["type"] == 'λ_abstraction':
        FV_λ_term = FV(N['λ_term'])
        FV_λ_term[ N['param'] ] = None
        return FV_λ_term

def generatorLetters():
    j = 0
    while True:
        x = []
        i = j
        while i != 0:
            x.insert(0, i%52)
            i //= 52
        if x == []: x = [0]
        st = map(lambda n: chr(96+26-n) if n<26 else chr(64+52-n), x)
        yield "".join(st)
        j += 1

def valNotIn(l):
    for val in generatorLetters():
        if val not in l:
            return val

def evaluate_primitive(pri, inputs, declarations):
    if pri == 'if':
        if len(inputs) != 3:
            raise Exception("if primitive need 3 lambda expresions")
        b = reduce_λ_term(inputs[0], declarations)
        if b['type'] != 'value' or type(b['value']) is not bool:
            raise Exception("if primitive require first expresion to be boolean")
        if b['value']:
            return reduce_λ_term(inputs[1], declarations)
        else:
            return reduce_λ_term(inputs[2], declarations)
