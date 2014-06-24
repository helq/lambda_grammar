def λ_term_to_str(λ_term):
    if λ_term['type'] == 'value':
        if type(λ_term['value']) is tuple:
            v1 = λ_term_to_str( λ_term['value'][0] )
            v2 = λ_term_to_str( λ_term['value'][1] )
            return "("+ str(v1) +":"+ str(v2) +")"
        if type(λ_term['value']) is bool:
            return "true" if λ_term['value'] else "false"
        if λ_term['value'] == None:
            return "nil"
        return repr(λ_term['value'])

    if λ_term['type'] == 'id': return λ_term['id']

    if λ_term['type'] == 'op':
        if isEnclosed(λ_term['op'], 'left', λ_term['val1']):
              val1 = "("+ λ_term_to_str(λ_term['val1']) +")"
        else: val1 =      λ_term_to_str(λ_term['val1'])

        if isEnclosed(λ_term['op'], 'right', λ_term['val2']):
              val2 = "("+ λ_term_to_str(λ_term['val2']) +")"
        else: val2 =      λ_term_to_str(λ_term['val2'])

        return ( val1 + λ_term['op'] + val2 )

    if λ_term['type'] == 'λ_abstraction':
        return ( "λ"
               + λ_term['param']
               + "."
               + λ_term_to_str(λ_term['λ_term']))

    if λ_term['type'] == 'λ_application':
        def sub_λ_term(term):
            if term['type'] in ['id', 'value']:
                  return       λ_term_to_str(term) + " "
            else: return "(" + λ_term_to_str(term) + ") "

        def sub_λ_term_f(term):
            if term['type'] == 'id': return       λ_term_to_str(term) + " "
            else:                    return "(" + λ_term_to_str(term) + ") "

        # del_if_last_is_space
        sp = lambda x: x[:-1] if x[-1] == ' ' else x

        func = sub_λ_term_f( λ_term['function'] )

        return func + sp( ''.join( map(sub_λ_term, λ_term['input']) ) )

operations = {
        '*': {'prec': 7, 'assoc': 'left'},
        '/': {'prec': 7, 'assoc': 'left'},
        '+': {'prec': 6, 'assoc': 'left'},
        '-': {'prec': 6, 'assoc': 'left'},
        ':': {'prec': 5, 'assoc': 'right'},
        '^': {'prec': 5, 'assoc': 'right'},
        '<': {'prec': 4, 'assoc': 'nonassoc'},
        '>': {'prec': 4, 'assoc': 'nonassoc'},
        '=': {'prec': 4, 'assoc': 'nonassoc'},
        '≠': {'prec': 4, 'assoc': 'nonassoc'},
        '&': {'prec': 3, 'assoc': 'left'},
        '|': {'prec': 3, 'assoc': 'left'},
}
def precedence(op): return operations[op]['prec']
def assoc(op):      return operations[op]['assoc']

def isEnclosed(op, side, valueOfSide):
    if valueOfSide['type'] in ['value', 'id', 'λ_application']:
        return False
    if valueOfSide['type'] == 'λ_abstraction':
        return True
    if valueOfSide['type'] == 'op':
        if   precedence( valueOfSide['op'] ) > precedence(op): return False
        elif precedence( valueOfSide['op'] ) < precedence(op): return True
        else:
            if assoc(op) == 'nonassoc': return True
            if assoc(op) == side: return False
            else:                 return True
