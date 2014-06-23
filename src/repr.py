from functools import reduce
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
        return ( "("
               + λ_term_to_str(λ_term['val1'])
               + λ_term['op']
               + λ_term_to_str(λ_term['val2'])
               + ")")

    if λ_term['type'] == 'λ_abstraction':
        return ( "λ"
               + λ_term['param']
               + "."
               + λ_term_to_str(λ_term['λ_term']))

    if λ_term['type'] == 'λ_application':
        def sub_λ_term(term):
            if   term['type'] == 'value': return str(term['value']) + " "
            elif term['type'] == 'id': return term['id'] + " "
            else:                      return "(" + λ_term_to_str(term) + ") "

        def sub_λ_term_f(term):
            if term['type'] == 'id': return term['id'] + " "
            else:                    return "(" + λ_term_to_str(term) + ") "

        # del_if_last_is_space
        sp = lambda x: x[:-1] if x[-1] == ' ' else x

        func = sub_λ_term_f( λ_term['function'] )

        return func + sp( ''.join( map(sub_λ_term, λ_term['input']) ) )
