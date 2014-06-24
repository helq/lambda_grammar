#-*- coding: utf-8 -*-
# module: interpreter.py
# author: helq
# license: wtfpl

from src.repr import λ_term_to_str
def printNothing(x): pass
call_by_value_substitution = True


primitives = ['if', 'fst', 'snd', 'show']

def reduce_λ_term(λ_term, declarations, myPrint=printNothing):
    what_happend=None

    # reduce lambda term until return something, or an error of types kill the
    # reducing
    while(True):
        myPrint( "= " + λ_term_to_str(λ_term)
               + (" " + what_happend if what_happend else "" )
               )
        what_happend=None

        # no more reduction posible
        if λ_term['type'] in ['value', 'λ_abstraction']:
            return λ_term

        # expresion with only a name variable, then replace variable with his
        # content (defined in declarations)
        if λ_term['type'] == 'id':
            if λ_term['id'] not in declarations:
                return λ_term
            λ_term = declarations[ λ_term['id'] ]
            continue

        # aplying an operation to two lambda terms
        if λ_term['type'] == 'op':
            op = λ_term['op']

            newMyPrint = lambda x: myPrint("  |"+x)

            # get value from first (left) lambda term
            if λ_term['val1']['type'] == 'value':
                value1 = λ_term['val1']
            else:
                myPrint( "  l-> " + λ_term_to_str(λ_term['val1']) )
                value1 = reduce_λ_term(λ_term['val1'], declarations, newMyPrint )

            # get value from second (right) lambda term
            if λ_term['val2']['type'] == 'value':
                value2 = λ_term['val2']
            else:
                myPrint( "  r-> " + λ_term_to_str(λ_term['val2']) )
                value2 = reduce_λ_term(λ_term['val2'], declarations, newMyPrint )

            λ_term = {'type': 'value', 'value': None} # value determined below

            # analyzing types of the values and determining the right value for
            # the new lambda term
            val1 = value1['value']
            val2 = value2['value']

            if op == ':': λ_term['value'] = (value1, value2)

            if op == '^':
                if type(val1) is not str or type(val2) is not str:
                    raise Exception("operator ^ only valid for strings")
                λ_term['value'] = val1 + val2

            if op in ['+', '-', '*', '/', '<', '>']:
                if type(val1) is not int or type(val2) is not int:
                    raise Exception("operator "+op+" only valid for numbers")
                if   op == '+': λ_term['value'] = val1 + val2
                elif op == '-': λ_term['value'] = val1 - val2
                elif op == '*': λ_term['value'] = val1 * val2
                elif op == '/': λ_term['value'] = val1 // val2
                elif op == '<': λ_term['value'] = val1 < val2
                elif op == '>': λ_term['value'] = val1 > val2

            if op in ['=', '≠']:
                if type(val1) != type(val2):
                    if (  not (type(val1) is tuple and val2 == None)
                      and not (type(val2) is tuple and val1 == None) ):
                        raise Exception("operator "+op+" need same type for the two expresions")
                if   op == '=': λ_term['value'] = val1 == val2
                elif op == '≠': λ_term['value'] = val1 != val2

            if op in ['&', '|']:
                if type(val1) is not bool or type(val2) is not bool:
                    raise Exception("operator "+op+" only valid for booleans")
                if   op == '&': λ_term['value'] = val1 and val2
                elif op == '|': λ_term['value'] = val1 or val2

            continue

        # the lambda term is an application. Now inside the function
        # application (the `f` inside `f s`) is possible find:
        # - a value, or operation
        # - a variable value
        # - another lambda application
        # - or a lambda abstraction
        if λ_term['type'] == 'λ_application':
            # this must be an error, but its better return
            if λ_term['function']['type'] in ["value", "op"]:
                return λ_term

            # if it's a variable value, than replace the variable by its
            # contents, using declaration or calling a primitive, if it's a
            # primitive function
            if λ_term['function']['type'] == "id":
                id = λ_term['function']['id']
                if id in primitives:
                    newMyPrint = lambda x: myPrint(" "+id+"|"+x)
                    λ_term = evaluate_primitive( id, λ_term['input']
                                               , declarations, newMyPrint)
                else:
                    λ_term['function'] = declarations[ id ]
                continue

            # another lambda application, than apply rule:
            # (f a ...) b ... ≡ f a ... b ...
            # (f a) b ≡ f a b
            if λ_term['function']['type'] == "λ_application":
                λ_term = { 'type': 'λ_application'
                         , 'function': λ_term['function']['function']
                         , 'input': λ_term['function']['input']+λ_term['input']}
                what_happend = "// left assoc λ aplications: (f x) y = f x y"
                continue

            # if it's a lambda abstraction, than apply a beta reduction
            if λ_term['function']['type'] == "λ_abstraction":
                param = λ_term['function']['param']
                term = λ_term['function']['λ_term']
                input_ = λ_term['input'][0]

                # β reduction: (λx.M) N ≡ M[x := N]
                new_λ_term = substitution(param, input_, declarations, myPrint) (term)
                what_happend = "// β-reduc"

                # (λx.M) N O ... ≡ (M[x := N]) O ...
                if len(λ_term['input']) > 1:
                    λ_term = { 'type': 'λ_application'
                             , 'function': new_λ_term
                             , 'input': λ_term['input'][1:] }
                # (λx.M) N ≡ M[x := N]
                else:
                    λ_term = new_λ_term

                continue


# subtitution, lambda calculus: M[x := N]
# https://en.wikipedia.org/wiki/Lambda_calculus#Substitution
def substitution(x, N, decls, myPrint=printNothing):
    if call_by_value_substitution:
        myPrint(" red|  "+ λ_term_to_str(N))
        N = reduce_λ_term(N, decls)
        myPrint(" red|= "+ λ_term_to_str(N))

    def subs_x_for_N_in(M):
        if M["type"] == 'value': return M # `value` [x := N] ≡ `value`
        if M["type"] == 'op': # (M1 `op` M2) [x := N] ≡ (M1[x := N] `op` M2[x := N])
            return { 'type': 'op'
                   , 'op': M['op']
                   , 'val1': subs_x_for_N_in(M['val1'])
                   , 'val2': subs_x_for_N_in(M['val2']) }

        if M["type"] == 'id':
            if M['id'] == x: return N # x[x := N] ≡ N
            else:            return M # y[x := N] ≡ y
        if M["type"] == 'λ_application': # (M1 M2)[x := N] ≡ (M1[x := N]) (M2[x := N])
            return { 'type': 'λ_application'
                   , 'function': subs_x_for_N_in(M['function'])
                   , 'input': list(map(subs_x_for_N_in, M['input'])) }
        if M["type"] == 'λ_abstraction':
            y = M['param']
            if y == x: return M # (λx.M)[x := N] ≡ λx.M
            else:
                if y in FV(N): # (λy.M)[x := N] ≡ λy.(M[x := N]), if x ≠ y
                               #  //IMPORTANT//                 , but y ∈ FV(N)

                    # in this case y ∈ FV(N), then is necesary change the name
                    # variable y for other that is not in the set of V(N) ∪ V(M)
                    V_M_plus_V_N = V(M)
                    V_M_plus_V_N.update( V(N) ) # V(N) ∪ V(M)
                    newY = valNotIn( V_M_plus_V_N ) # newY ∉ V(N) ∪ V(M)
                    newYid = { 'type': 'id', 'id': newY }

                    myPrint( "        |= " + λ_term_to_str(M) )
                    M = { 'type': 'λ_abstraction'
                        , 'param': newY
                        , 'λ_term': substitution(y, newYid, decls)(M['λ_term'])
                        }
                    myPrint( " α-reduc|= " + λ_term_to_str(M) )
                    # now: (λ newY.M)[x := N] ≡ λ newY.(M[x := N]), if x ≠ newY
                    #                                             , provided newY ∉ FV(N)

                # (λy.M)[x := N] ≡ λy.(M[x := N]), if x ≠ y
                #                                , provided y ∉ FV(N)
                return { 'type': 'λ_abstraction'
                       , 'param': M['param']
                       , 'λ_term': subs_x_for_N_in(M['λ_term'])
                       }
    return subs_x_for_N_in

# Free-variables in the lambda term N
# https://en.wikipedia.org/wiki/Lambda_calculus#Free_and_bound_variables
def FV(N):
    if N['type'] == 'value': return {} # FV(`value`) = {}
    if N['type'] == 'op': # FV(M `op` N) = FV(M) ∪ FV(N)
        FV_val1 = FV(N['val1'])
        FV_val2 = FV(N['val2'])
        FV_val1.update(FV_val2)
        return FV_val1

    if N['type'] == 'id':    return {N['id']: None} # FV(x) = {x}, where x is a variable
    if N['type'] == 'λ_application': # FV(M N) = FV(M) ∪ FV(N)
        FV_function = FV(N['function'])
        FV_input = list(map(FV, N['input']))
        for i in FV_input:
            FV_function.update(i)
        return FV_function
    if N["type"] == 'λ_abstraction': # FV(λx.M) = FV(M) \ {x}
        FV_λ_term = FV(N['λ_term'])
        del( FV_λ_term[ N['param'] ] )
        return FV_λ_term

# Variables (free and bound variables) in the lambda term N
# same implementation as FV(N), except for rule: FV(λx.M) = FV(M) \ {x}
# that is now: V(λx.M) = V(M) ∪ {x}
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

# this create a iterator with many possible name variables
# generatorLetters ≈ ['z', 'y', 'x', 'w', 'v', ...]
def generatorLetters():
    from itertools import count
    for j in count():
        x = [0]
        i = j
        while i != 0:
            x.insert(0, i%52)
            i //= 52
        if x == []: x = [0]
        st = map(lambda n: chr(96+26-n) if n<26 else chr(64+52-n), x)
        yield "".join(st)

# with a set `l` of name variables (strings), find a name variable that is not
# in the set
def valNotIn(l):
    for val in generatorLetters():
        if val not in l:
            return val

def evaluate_primitive(pri, inputs, declarations, myPrint):
    if pri == 'if':
        if len(inputs) < 3:
            raise Exception("`if` primitive need 3 lambda expresions to work")

        b = reduce_λ_term(inputs[0], declarations, myPrint)
        if b['type'] != 'value' or type(b['value']) is not bool:
            raise Exception("`if` primitive require first expresion to be a boolean")

        if len(inputs) > 3:
            return { 'type': 'λ_application'
                   , 'function': inputs[1] if b['value'] else inputs[2]
                   , 'input': inputs[3:] }
        else: # len(inputs) == 3
            return inputs[1] if b['value'] else inputs[2]

    if pri in ['fst', 'snd']:
        cons = reduce_λ_term(inputs[0], declarations, myPrint)
        if cons['type'] == 'value' and cons['value'] == None:
            raise Exception("`"+pri+"` applied to a `nil`, imposible")
        if cons['type'] != 'value' or type(cons['value']) is not tuple:
            raise Exception("`"+pri+"` primitive require expresion to be a cons")

        if len(inputs) > 1:
            raise Exception("`"+pri+"` can only be applied to one expresion")
        else: # len(inputs) == 1
            if   pri == "fst":
                return cons['value'][0]
            elif pri == "snd":
                return cons['value'][1]

    if pri == 'show':
        if len(inputs) > 1:
            raise Exception("`"+pri+"` can only be applied to one expresion")
        toShow = reduce_λ_term(inputs[0], declarations, myPrint)
        return {'type': 'value', 'value': λ_term_to_str(toShow)}
