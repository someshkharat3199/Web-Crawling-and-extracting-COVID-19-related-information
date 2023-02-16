
tokens = [
    'NEWCASES',
    'SEP1',
    'SEP2',
    'ACTIVECASES',
    'DEATHCASES',
    'RECOVERY',
    'END',
    'DATA',
    'DATE'
]

def t_NEWCASES(t):
    r'<!DOCTYPE\shtml>[\S\s]+<div\sid="graph-cases-daily"></div>'
    return t

def t_SEP2(t):
    r'yAxis:[\S\s]+?data:\s\['
    return t

def t_ACTIVECASES(t):
    r'responsive:[\S\s]+<div\sid="graph-active-cases-total"></div>'
    return t


def t_DEATHCASES(t):
    r'responsive:[\S\s]+<div\sid="graph-deaths-daily"></div>'
    return t

def t_RECOVERY(t):
    r'responsive:[\S\s]+<div\sid="cases-cured-daily"></div>'
    return t

def t_SEP1(t):
    r'<script\stype="text/javascript">[\S\s]+?categories:\s\['
    return t



def t_END(t):
    r'responsive:[\S\s]+</html>'
    return t    

def t_DATA(t):
    r'[0-9,\-null]{5,}'
    return t

def t_DATE(t):
    r'\"[A-Za-z0-9,\s]+\"'
    return t

t_ignore = ' \t'

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
     
def t_error(t):
    t.lexer.skip(1)
    
#grammar rules

def p_start(t):
    'start : newcases activecases deathcases recovery END'
    t[0] = {'new': t[1],'active' : t[2],'death' : t[3],'recovery' : t[4]}
    
def p_pnewcases(t):
    'newcases : NEWCASES SEP1 pdates SEP2 pdata pdata pdata'
    t[0] = {'dates' : t[3].split('|'), 'data' : t[5].split(',')}
    
def p_activecases(t):
    '''activecases : ACTIVECASES SEP1 pdates SEP2 pdata
                   | '''
    if(len(t) == 6):
        t[0] = {'dates' : t[3].split('|'), 'data' : t[5].split(',')}
    else:
        t[0] = {'dates':[],'data':[]}
    
def p_deathcases(t):
    '''deathcases : DEATHCASES SEP1 pdates SEP2 pdata pdata pdata
                | '''
    if(len(t) == 8):
        t[0] = {'dates' : t[3].split('|'), 'data' : t[5].split(',')}
    else:
        t[0] = {'dates':[],'data':[]} 

     
def p_recovery(t):
    '''recovery : RECOVERY SEP1 pdates SEP2 pdata pdata
                | '''
    if(len(t) == 7):
        t[0] = {'dates': t[3].split('|'),'data' : t[5].split(',')}
    else:
        t[0] = {'dates':[],'data':[]}
    
def p_pdates(t):
    '''pdates : DATE
              | DATE pdates'''
    if(len(t) == 2):
        t[0] = t[1].strip('"')
    if(len(t) == 3):
        t[0] = t[1].strip('"') +'|'+ t[2].strip('"')
              
def p_pdata(t):
    'pdata : DATA'
    t[0] = t[1]

def p_error(t):
    # print(t)
    pass  