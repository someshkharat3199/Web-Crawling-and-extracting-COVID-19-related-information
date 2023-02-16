tokens = [
    'START',
    'END',
    'LUL',
    'RUL',
    'LLI',
    'RLI',
    'LANCHOR',
    'RANCHOR',
    'INDEX'
]

def t_START(t):
    r'<!DOCTYPE\shtml>[\S\s]+?England">edit</a><span\sclass="mw-editsection-bracket">]</span></span></h3>'
    return t

def t_END(t):
    r'<h3><span\sclass="mw-headline"\sid="Northern_Ireland">Northern\sIreland[\S\s]+?</html>'
    return t
    
def t_LUL(t):
    r'<ul>'
    return t

def t_RUL(t):
    r'</ul>'
    return t

def t_LLI(t):
    r'<li>'
    return t

def t_RLI(t):
    r'</li>'
    return t

def t_LANCHOR(t):
    r'<a\s[^>]+?>'
    return t

def t_RANCHOR(t):
    r'</a>'
    return t

def t_INDEX(t):
    r'[A-za-z0-9\(\) ]+'
    return t

t_ignore = ' \t'

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
     
def t_error(t):
    t.lexer.skip(1)
    
#grammer_rules
def p_start(t):
    'start : START ulist END'
    t[0] = t[2]
    
def p_ulist(t):
    'ulist : LUL llist RUL'
    t[0] = t[2]
    
    
def p_llist(t):
    '''llist : LLI LANCHOR index RANCHOR RLI
             '''
    if(len(t) == 6):
        t[0] = {t[3] : t[2]}
        
def p_multilist(t):
    '''llist : LLI LANCHOR index RANCHOR RLI llist
             '''
    if(len(t) == 7):
        if(t[6] == None):
            t[0] = {t[3]:t[2]}
        else:
            t[0] = {**{t[3]:t[2]},**t[6]}
def p_index(t):
    '''index : INDEX
             | INDEX index
             ''' 
    if(len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = t[1] +' '+ t[2]
    

def p_error(t):
    # print(t,t.lineno)
    pass  