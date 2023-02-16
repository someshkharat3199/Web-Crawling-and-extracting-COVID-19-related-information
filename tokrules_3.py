
tokens = [
    'NLINKS',
    'RLINKS',
    'CLINKS',
    'END',
    'LUL',
    'RUL',
    'LLI',
    'RLI',
    'LANCHOR',
    'RANCHOR',
    'INDEX'
]

def t_NLINKS(t):
    r'<!DOCTYPE\shtml>[\S\s]+?timelines\sof\sthe\sCOVID-19\spandemic\srespectively\sin:\s\s</p>'
    return t

def t_RLINKS(t):
    r'<dl><dt>Responses[\S\s]+responses\sto\sthe\sCOVID-19\spandemic\srespectively\sin:\s</p>'
    return t

def t_CLINKS(t):
    r'<h2><span\sclass="mw-headline"\sid="Timeline_by_country[\S\s]+timeline\sof\sthe\sCOVID-19\spandemic\sin:\s</p>'
    return t

def t_END(t):
    r'<h2><span\sclass="mw-headline"\sid="Worldwide_cases_by_month_and_year[\S\s]+</html>'
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
    
#grammar rules

def p_start(t):
    'start : NLINKS ulist RLINKS ulist CLINKS ulist END'
    t[0] = {'world_news': t[2],'responses' : t[4],'country_news' : t[6]}
    
def p_ulist(t):
    'ulist : LUL llist RUL'
    t[0] = t[2]
    
    
def p_llist(t):
    '''llist : LLI LANCHOR index RANCHOR RLI
             | LLI index ulist RLI
             | LLI LANCHOR index RANCHOR ulist RLI
             '''
    if(len(t) == 6):
        t[0] = {t[3] : t[2]}
    if(len(t) == 5):
        t[0] = {t[2] : t[3]}
    if(len(t) == 7):
        t[0] = {t[3] : {'main_link':t[2] ,'other': t[5]}}
        
def p_multilist(t):
    '''llist : LLI LANCHOR index RANCHOR RLI llist
             | LLI index ulist RLI llist
             | LLI LANCHOR index RANCHOR ulist RLI llist
             '''
    if(len(t) == 8):
        if(t[7] == None):
            t[0] = {t[3] : {'main_link':t[2] ,'other': t[5]}}
        else:
            t[0] = {**t[7],**{t[3] : {'main_link':t[2] ,'other': t[5]}}}
    if(len(t) == 7):
        if(t[6] == None):
            t[0] = {t[3]:t[2]}
        else:
            t[0] = {**t[6],**{t[3]:t[2]}}
    if(len(t) == 6):
        if(t[5] == None):
            t[0] = {t[2]:t[3]}
        else:
            t[0] = {**t[5],**{t[2]:t[3]}}

def p_index(t):
    '''index : INDEX
             | INDEX index
             ''' 
    if(len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = t[1] +' '+ t[2]
    

def p_error(t):
    # print(t)
    pass  